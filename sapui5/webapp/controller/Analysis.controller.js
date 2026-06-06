sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageBox",
    "sap/m/Button",
    "sap/m/VBox",
    "sap/m/HBox",
    "sap/m/Text",
    "sap/m/Title",
    "sap/m/Table",
    "sap/m/Column",
    "sap/m/ColumnListItem",
    "sap/m/ObjectStatus",
    "ewa/analyzer/model/config"
], function (Controller, JSONModel, MessageBox, Button, VBox, HBox, Text, Title, Table, Column, ColumnListItem, ObjectStatus, Config) {
    "use strict";

    var DOMAIN_LABELS = {
        security: "Security",
        database: "Database",
        performance: "Performance",
        basis: "Basis / Technical",
        business: "Business",
        lifecycle: "Lifecycle Management"
    };

    var NUMBER_FORMATTER = new Intl.NumberFormat("en-GB");
    var CURRENCY_FORMATTER = new Intl.NumberFormat("en-GB", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 4,
        maximumFractionDigits: 6
    });

    return Controller.extend("ewa.analyzer.controller.Analysis", {

        onInit: function () {
            this.getView().setModel(new JSONModel({
                title: "",
                reportDate: ""
            }), "analysis");

            this.getOwnerComponent().getRouter().getRoute("Preview").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function (oEvent) {
            var sBaseName = oEvent.getParameter("arguments").baseName;
            this._sBaseName = sBaseName;
            this._sWorkbookName = sBaseName + "_workbook.xlsx";
            this._sPayloadName = sBaseName + "_workbook_payload.json";
            this._sUsageName = sBaseName + "_v2_usage.json";

            this._loadAnalysisArtifacts();
        },

        _loadAnalysisArtifacts: function () {
            var that = this;

            this.getView().setBusy(true);

            Promise.all([
                this._fetchRequiredJson(this._sPayloadName),
                this._fetchOptionalJson(this._sUsageName)
            ])
                .then(function (aResults) {
                    that._renderWorkbookSummary(aResults[0], aResults[1]);
                })
                .catch(function (err) {
                    MessageBox.error("Failed to load analysis results: " + err.message);
                })
                .finally(function () {
                    that.getView().setBusy(false);
                });
        },

        _fetchRequiredJson: function (sBlobName) {
            return fetch(Config.getDownloadUrl(sBlobName))
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("Artifact not found (HTTP " + response.status + ")");
                    }
                    return response.json();
                });
        },

        _fetchOptionalJson: function (sBlobName) {
            return fetch(Config.getDownloadUrl(sBlobName))
                .then(function (response) {
                    if (response.status === 404) {
                        return null;
                    }
                    if (!response.ok) {
                        throw new Error("Usage artifact could not be loaded (HTTP " + response.status + ")");
                    }
                    return response.json();
                });
        },

        _renderWorkbookSummary: function (payload, usage) {
            var oContainer = this.byId("reportContainer");
            oContainer.destroyItems();

            var aDomainResults = payload.domain_results || payload.domain_analyses || [];
            var aSupplemental = payload.supplemental_findings || payload.cross_references || [];

            var totalRed = 0;
            var totalAmber = 0;
            var totalFindings = 0;
            var totalParams = 0;

            aDomainResults.forEach(function (dr) {
                var aF = dr.findings || [];
                totalFindings += aF.length;
                totalParams += (dr.parameters || []).length;
                aF.forEach(function (f) {
                    var s = (f.rag_status || f.severity || "").toUpperCase();
                    if (s === "RED" || s === "CRITICAL" || s === "HIGH") {
                        totalRed++;
                    } else if (s === "AMBER" || s === "YELLOW" || s === "MEDIUM" || s === "WARNING") {
                        totalAmber++;
                    }
                });
            });

            oContainer.addItem(new Title({
                text: "EWA Workbook Analysis",
                level: "H1"
            }).addStyleClass("sapUiMediumMarginBottom markdown-header-1"));

            oContainer.addItem(new HBox({
                wrap: "Wrap",
                items: [
                    this._makeStat(String(totalRed), "Critical / RED", "Error"),
                    this._makeStat(String(totalAmber), "Warnings / AMBER", "Warning"),
                    this._makeStat(String(totalFindings), "Total Findings", "None"),
                    this._makeStat(String(totalParams), "Parameters", "None"),
                    this._makeStat(String(aSupplemental.length), "Cross-Domain", "Information")
                ]
            }).addStyleClass("sapUiMediumMarginBottom"));

            this._renderUsageSummary(oContainer, usage);

            oContainer.addItem(new Button({
                text: "Download EWA Workbook (.xlsx)",
                icon: "sap-icon://excel-attachment",
                type: "Emphasized",
                press: this.onDownloadWorkbook.bind(this)
            }).addStyleClass("sapUiSmallMarginBottom"));

            oContainer.addItem(new Title({
                text: "Findings by Domain",
                level: "H2"
            }).addStyleClass("sapUiSmallMarginTop sapUiTinyMarginBottom markdown-header-2"));

            var oTable = new Table({ width: "100%", fixedLayout: false }).addStyleClass("sapUiSmallMarginBottom");
            ["Domain", "RED", "AMBER", "GREEN", "Findings", "Parameters"].forEach(function (sHeader) {
                oTable.addColumn(new Column({
                    header: new Text({ text: sHeader, wrapping: false }),
                    minScreenWidth: "Tablet",
                    demandPopin: true
                }));
            });

            aDomainResults.forEach(function (dr) {
                var aF = dr.findings || [];
                var red = 0;
                var amber = 0;
                var green = 0;

                aF.forEach(function (f) {
                    var s = (f.rag_status || f.severity || "").toUpperCase();
                    if (s === "RED" || s === "CRITICAL" || s === "HIGH") {
                        red++;
                    } else if (s === "AMBER" || s === "YELLOW" || s === "MEDIUM" || s === "WARNING") {
                        amber++;
                    } else {
                        green++;
                    }
                });

                var sDomainKey = dr.domain || dr.section_title || "";
                var sLabel = DOMAIN_LABELS[sDomainKey] || sDomainKey;
                var oItem = new ColumnListItem();
                oItem.addCell(new Text({ text: sLabel }));
                oItem.addCell(new ObjectStatus({ text: String(red), state: red > 0 ? "Error" : "None" }));
                oItem.addCell(new ObjectStatus({ text: String(amber), state: amber > 0 ? "Warning" : "None" }));
                oItem.addCell(new Text({ text: String(green) }));
                oItem.addCell(new Text({ text: String(aF.length) }));
                oItem.addCell(new Text({ text: String((dr.parameters || []).length) }));
                oTable.addItem(oItem);
            });
            oContainer.addItem(oTable);

            if (aSupplemental.length > 0) {
                oContainer.addItem(new Title({
                    text: "Cross-Domain Supplemental Findings (" + aSupplemental.length + ")",
                    level: "H2"
                }).addStyleClass("sapUiSmallMarginTop sapUiTinyMarginBottom markdown-header-2"));

                var oSupTable = new Table({ width: "100%" }).addStyleClass("sapUiSmallMarginBottom");
                ["Severity", "Title", "Finding"].forEach(function (sHeader) {
                    oSupTable.addColumn(new Column({
                        header: new Text({ text: sHeader, wrapping: false }),
                        minScreenWidth: "Tablet",
                        demandPopin: true
                    }));
                });

                aSupplemental.forEach(function (sf) {
                    var sev = (sf.severity || sf.rag_status || "INFO").toUpperCase();
                    var sevState = (sev === "CRITICAL" || sev === "HIGH" || sev === "RED") ? "Error"
                        : (sev === "MEDIUM" || sev === "AMBER" || sev === "YELLOW") ? "Warning" : "None";
                    var oSupItem = new ColumnListItem();
                    oSupItem.addCell(new ObjectStatus({ text: sev, state: sevState }));
                    oSupItem.addCell(new Text({ text: sf.title || sf.finding_title || "", wrapping: true }));
                    oSupItem.addCell(new Text({ text: sf.finding || sf.description || sf.correlation_description || "", wrapping: true }));
                    oSupTable.addItem(oSupItem);
                });
                oContainer.addItem(oSupTable);
            }

            oContainer.addItem(new Button({
                text: "Download EWA Workbook (.xlsx)",
                icon: "sap-icon://excel-attachment",
                type: "Emphasized",
                press: this.onDownloadWorkbook.bind(this)
            }).addStyleClass("sapUiMediumMarginTop"));
        },

        _renderUsageSummary: function (oContainer, oUsage) {
            if (!oUsage || !oUsage.totals) {
                oContainer.addItem(new VBox({
                    items: [
                        new Title({
                            text: "Run Usage & Cost",
                            level: "H2"
                        }).addStyleClass("sapUiTinyMarginBottom markdown-header-2"),
                        new Text({
                            text: "Usage and cost telemetry is not available for this analysis run.",
                            wrapping: true
                        })
                    ]
                }).addStyleClass("ewaUsageCard sapUiMediumMarginBottom"));
                return;
            }

            var oTotals = oUsage.totals || {};
            var aBreakdown = oUsage.breakdown || [];
            var oRun = oUsage.run || {};

            oContainer.addItem(new Title({
                text: "Run Usage & Cost",
                level: "H2"
            }).addStyleClass("sapUiSmallMarginTop sapUiTinyMarginBottom markdown-header-2"));

            oContainer.addItem(new HBox({
                wrap: "Wrap",
                items: [
                    this._makeStat(this._formatNumber(oTotals.input_tokens), "Input Tokens", "None"),
                    this._makeStat(this._formatNumber(oTotals.cached_input_tokens), "Cached Input", "Information"),
                    this._makeStat(this._formatNumber(oTotals.output_tokens), "Output Tokens", "None"),
                    this._makeStat(this._formatNumber(oTotals.total_tokens), "Total Tokens", "None"),
                    this._makeStat(this._formatCurrency(oTotals.cost_usd), "Run Cost (USD)", "Success"),
                    this._makeStat(this._formatDuration(oRun.duration_seconds), "Duration", "Information")
                ]
            }).addStyleClass("sapUiSmallMarginBottom"));

            var oUsageTable = new Table({ width: "100%", fixedLayout: false }).addStyleClass("sapUiSmallMarginBottom");
            ["Phase", "Model", "Calls", "Input", "Cached", "Billable", "Output", "Cost"].forEach(function (sHeader) {
                oUsageTable.addColumn(new Column({
                    header: new Text({ text: sHeader, wrapping: false }),
                    minScreenWidth: "Tablet",
                    demandPopin: true
                }));
            });

            aBreakdown.forEach(function (oEntry) {
                var oItem = new ColumnListItem();
                oItem.addCell(new Text({ text: this._formatPhaseLabel(oEntry.phase), wrapping: true }));
                oItem.addCell(new Text({ text: oEntry.model || "", wrapping: true }));
                oItem.addCell(new Text({ text: this._formatNumber(oEntry.calls) }));
                oItem.addCell(new Text({ text: this._formatNumber(oEntry.input_tokens) }));
                oItem.addCell(new Text({ text: this._formatNumber(oEntry.cached_input_tokens) }));
                oItem.addCell(new Text({ text: this._formatNumber(oEntry.billable_input_tokens) }));
                oItem.addCell(new Text({ text: this._formatNumber(oEntry.output_tokens) }));
                oItem.addCell(new ObjectStatus({
                    text: this._formatCurrency(oEntry.total_cost_usd),
                    state: (oEntry.total_cost_usd || 0) > 0 ? "Success" : "None"
                }));
                oUsageTable.addItem(oItem);
            }.bind(this));
            oContainer.addItem(oUsageTable);

            if ((oUsage.notes || []).length > 0) {
                var oNotesBox = new VBox().addStyleClass("ewaUsageCard sapUiMediumMarginBottom");
                oNotesBox.addItem(new Text({
                    text: "Notes",
                    wrapping: false
                }).addStyleClass("ewaUsageNotesTitle"));

                (oUsage.notes || []).forEach(function (sNote) {
                    oNotesBox.addItem(new Text({
                        text: sNote,
                        wrapping: true
                    }).addStyleClass("ewaUsageNoteItem"));
                });

                oContainer.addItem(oNotesBox);
            }
        },

        _makeStat: function (sValue, sLabel, sState) {
            return new VBox({
                alignItems: "Center",
                items: [
                    new ObjectStatus({
                        text: sValue,
                        state: sState || "None"
                    }).addStyleClass("ewaStatValue"),
                    new Text({ text: sLabel }).addStyleClass("ewaStatLabel")
                ]
            }).addStyleClass("ewaStatCard sapUiSmallMarginEnd sapUiSmallMarginBottom");
        },

        _formatNumber: function (vValue) {
            return NUMBER_FORMATTER.format(Number(vValue || 0));
        },

        _formatCurrency: function (vValue) {
            return CURRENCY_FORMATTER.format(Number(vValue || 0));
        },

        _formatPhaseLabel: function (sPhase) {
            var oLabels = {
                phase0_planning: "Planning",
                phase1_domain_analysis: "Domain Analysis",
                phase2_cross_reference: "Cross-Reference",
                phase2_synthesis: "Final Synthesis"
            };

            return oLabels[sPhase] || (sPhase || "");
        },

        _formatDuration: function (vSeconds) {
            var nSeconds = Number(vSeconds || 0);
            if (!nSeconds) {
                return "n/a";
            }
            if (nSeconds < 60) {
                return nSeconds.toFixed(1) + "s";
            }
            return (nSeconds / 60).toFixed(1) + "m";
        },

        onDownloadWorkbook: function () {
            window.open(Config.getDownloadUrl(this._sWorkbookName), "_blank");
        },

        onNavBack: function () {
            this.getOwnerComponent().getRouter().navTo("Main");
        }
    });
});
