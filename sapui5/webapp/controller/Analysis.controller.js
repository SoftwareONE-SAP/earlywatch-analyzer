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
    var OPENAI_FALLBACK_PRICING = {
        "gpt-5.6-sol": {
            input_per_1m: 5.00,
            cached_input_per_1m: 0.50,
            cache_write_per_1m: 6.25,
            output_per_1m: 30.00
        },
        "gpt-5.6-terra": {
            input_per_1m: 2.50,
            cached_input_per_1m: 0.25,
            cache_write_per_1m: 3.125,
            output_per_1m: 15.00
        },
        "gpt-5.6-luna": {
            input_per_1m: 1.00,
            cached_input_per_1m: 0.10,
            cache_write_per_1m: 1.25,
            output_per_1m: 6.00
        },
        "gpt-5.6": {
            input_per_1m: 5.00,
            cached_input_per_1m: 0.50,
            cache_write_per_1m: 6.25,
            output_per_1m: 30.00
        },
        "gpt-5.4": {
            input_per_1m: 2.50,
            cached_input_per_1m: 0.25,
            output_per_1m: 15.00
        },
        "gpt-5.4-mini": {
            input_per_1m: 0.75,
            cached_input_per_1m: 0.075,
            output_per_1m: 4.50
        },
        "gpt-5.4-nano": {
            input_per_1m: 0.20,
            cached_input_per_1m: 0.02,
            output_per_1m: 1.25
        }
    };

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

            this._fetchRequiredJson(this._sPayloadName)
                .then(function (oPayload) {
                    return that._loadUsageArtifact()
                        .then(function (oUsage) {
                            that._renderWorkbookSummary(oPayload, oUsage || that._usageFromPayload(oPayload));
                        });
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
                    if (!response.ok) {
                        return null;
                    }
                    return response.json();
                })
                .catch(function () {
                    return null;
                });
        },

        _loadUsageArtifact: function () {
            var aCandidates = [
                this._sUsageName,
                this._sBaseName + "_usage.json",
                this._sBaseName + "_workbook_cost.json"
            ];

            var fnTryNext = function (iIndex) {
                if (iIndex >= aCandidates.length) {
                    return Promise.resolve(null);
                }

                return this._fetchOptionalJson(aCandidates[iIndex])
                    .then(function (oUsage) {
                        return oUsage || fnTryNext(iIndex + 1);
                    });
            }.bind(this);

            return fnTryNext(0);
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
            oUsage = this._withComputedCosts(oUsage);

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
                    this._makeStat(this._formatNumber(oTotals.cache_write_tokens), "Cache Write", "Information"),
                    this._makeStat(this._formatNumber(oTotals.output_tokens), "Output Tokens", "None"),
                    this._makeStat(this._formatNumber(oTotals.total_tokens), "Total Tokens", "None"),
                    this._makeStat(this._formatCurrency(oTotals.cost_usd), "Run Cost (USD)", "Success"),
                    this._makeStat(this._formatDuration(oRun.duration_seconds), "Duration", "Information")
                ]
            }).addStyleClass("sapUiSmallMarginBottom"));

            var oUsageTable = new Table({ width: "100%", fixedLayout: false }).addStyleClass("sapUiSmallMarginBottom");
            ["Phase", "Model", "Calls", "Input", "Cached", "Cache Write", "Billable", "Output", "Cost"].forEach(function (sHeader) {
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
                oItem.addCell(new Text({ text: this._formatNumber(oEntry.cache_write_tokens) }));
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

        _withComputedCosts: function (oUsage) {
            if (!oUsage || !oUsage.totals) {
                return oUsage;
            }

            var bUsedFallbackPricing = false;
            var nTotalCost = 0;
            var aBreakdown = (oUsage.breakdown || []).map(function (oEntry) {
                var oPricedEntry = Object.assign({}, oEntry);
                var oPricing = this._pricingForEntry(oPricedEntry);
                var nInputTokens = Number(oPricedEntry.input_tokens || 0);
                var nCachedInputTokens = Number(oPricedEntry.cached_input_tokens || 0);
                var nCacheWriteTokens = Number(oPricedEntry.cache_write_tokens || 0);
                var nOutputTokens = Number(oPricedEntry.output_tokens || 0);
                var nBillableInputTokens = Math.max(
                    Number(oPricedEntry.billable_input_tokens || 0) || (nInputTokens - nCachedInputTokens - nCacheWriteTokens),
                    0
                );

                oPricedEntry.billable_input_tokens = nBillableInputTokens;

                if (oPricing) {
                    bUsedFallbackPricing = bUsedFallbackPricing || this._entryHasZeroPricing(oEntry);
                    oPricedEntry.pricing = oPricing;
                    oPricedEntry.input_cost_usd = this._roundCost(nBillableInputTokens / 1000000 * oPricing.input_per_1m);
                    oPricedEntry.cached_input_cost_usd = this._roundCost(nCachedInputTokens / 1000000 * oPricing.cached_input_per_1m);
                    oPricedEntry.cache_write_cost_usd = this._roundCost(nCacheWriteTokens / 1000000 * oPricing.cache_write_per_1m);
                    oPricedEntry.output_cost_usd = this._roundCost(nOutputTokens / 1000000 * oPricing.output_per_1m);
                    oPricedEntry.total_cost_usd = this._roundCost(
                        oPricedEntry.input_cost_usd +
                        oPricedEntry.cached_input_cost_usd +
                        oPricedEntry.cache_write_cost_usd +
                        oPricedEntry.output_cost_usd
                    );
                }

                nTotalCost += Number(oPricedEntry.total_cost_usd || 0);
                return oPricedEntry;
            }.bind(this));

            var oTotals = Object.assign({}, oUsage.totals, {
                cost_usd: this._roundCost(nTotalCost)
            });
            var aNotes = (oUsage.notes || []).filter(function (sNote) {
                return sNote.indexOf("No pricing configured for model") === -1;
            });

            if (bUsedFallbackPricing) {
                aNotes.push("Costs were calculated in the UI from OpenAI standard API pricing for known model names.");
            }

            return Object.assign({}, oUsage, {
                breakdown: aBreakdown,
                totals: oTotals,
                notes: aNotes
            });
        },

        _pricingForEntry: function (oEntry) {
            var sModel = this._normalizeModelName(oEntry.model);
            var oCurrentPricing = oEntry.pricing || {};
            var oFallbackPricing = OPENAI_FALLBACK_PRICING[sModel];

            if (!this._entryHasZeroPricing(oEntry)) {
                return {
                    input_per_1m: Number(oCurrentPricing.input_per_1m || 0),
                    cached_input_per_1m: Number(oCurrentPricing.cached_input_per_1m || 0),
                    cache_write_per_1m: Number(oCurrentPricing.cache_write_per_1m || (oFallbackPricing && oFallbackPricing.cache_write_per_1m) || 0),
                    output_per_1m: Number(oCurrentPricing.output_per_1m || 0)
                };
            }

            return oFallbackPricing || null;
        },

        _entryHasZeroPricing: function (oEntry) {
            var oPricing = oEntry.pricing || {};

            return !Number(oPricing.input_per_1m || 0) &&
                !Number(oPricing.cached_input_per_1m || 0) &&
                !Number(oPricing.cache_write_per_1m || 0) &&
                !Number(oPricing.output_per_1m || 0);
        },

        _normalizeModelName: function (sModel) {
            var sValue = String(sModel || "").toLowerCase();

            if (sValue.indexOf("gpt-5.6-luna") !== -1) {
                return "gpt-5.6-luna";
            }
            if (sValue.indexOf("gpt-5.6-terra") !== -1) {
                return "gpt-5.6-terra";
            }
            if (sValue.indexOf("gpt-5.6-sol") !== -1) {
                return "gpt-5.6-sol";
            }
            if (sValue.indexOf("gpt-5.6") !== -1) {
                return "gpt-5.6";
            }
            if (sValue.indexOf("gpt-5.4-mini") !== -1) {
                return "gpt-5.4-mini";
            }
            if (sValue.indexOf("gpt-5.4-nano") !== -1) {
                return "gpt-5.4-nano";
            }
            if (sValue.indexOf("gpt-5.4") !== -1) {
                return "gpt-5.4";
            }

            return sValue;
        },

        _roundCost: function (nValue) {
            return Math.round(Number(nValue || 0) * 1000000) / 1000000;
        },

        _usageFromPayload: function (oPayload) {
            var oTokenUsage = oPayload && oPayload.token_usage;
            if (!oTokenUsage) {
                return null;
            }

            var aBreakdown = [
                this._usageEntryFromPayload(
                    "phase0_planning",
                    oTokenUsage.phase0_model || "gpt-5.4",
                    oTokenUsage.phase0_input_tokens,
                    oTokenUsage.phase0_cached_input_tokens,
                    oTokenUsage.phase0_cache_write_tokens,
                    oTokenUsage.phase0_output_tokens
                ),
                this._usageEntryFromPayload(
                    "phase1_domain_analysis",
                    oTokenUsage.phase1_model || "gpt-5.4-mini",
                    oTokenUsage.phase1_input_tokens,
                    oTokenUsage.phase1_cached_input_tokens,
                    oTokenUsage.phase1_cache_write_tokens,
                    oTokenUsage.phase1_output_tokens
                ),
                this._usageEntryFromPayload(
                    "phase2_synthesis",
                    oTokenUsage.phase2_model || "gpt-5.4",
                    oTokenUsage.phase2_input_tokens,
                    oTokenUsage.phase2_cached_input_tokens,
                    oTokenUsage.phase2_cache_write_tokens,
                    oTokenUsage.phase2_output_tokens
                )
            ];

            var oTotals = aBreakdown.reduce(function (oAcc, oEntry) {
                oAcc.input_tokens += oEntry.input_tokens;
                oAcc.cached_input_tokens += oEntry.cached_input_tokens;
                oAcc.cache_write_tokens += oEntry.cache_write_tokens;
                oAcc.billable_input_tokens += oEntry.billable_input_tokens;
                oAcc.output_tokens += oEntry.output_tokens;
                oAcc.total_tokens += oEntry.input_tokens + oEntry.output_tokens;
                return oAcc;
            }, {
                calls: 0,
                input_tokens: 0,
                cached_input_tokens: 0,
                cache_write_tokens: 0,
                billable_input_tokens: 0,
                output_tokens: 0,
                total_tokens: 0,
                cost_usd: 0
            });

            return {
                breakdown: aBreakdown,
                totals: oTotals,
                notes: [
                    "Detailed usage JSON was not available; showing token totals embedded in the workbook payload."
                ]
            };
        },

        _usageEntryFromPayload: function (sPhase, sModel, iInput, iCachedInput, iCacheWrite, iOutput) {
            var nInput = Number(iInput || 0);
            var nCachedInput = Number(iCachedInput || 0);
            var nCacheWrite = Number(iCacheWrite || 0);
            var nOutput = Number(iOutput || 0);

            return {
                phase: sPhase,
                model: sModel,
                calls: 0,
                input_tokens: nInput,
                cached_input_tokens: nCachedInput,
                cache_write_tokens: nCacheWrite,
                billable_input_tokens: Math.max(nInput - nCachedInput - nCacheWrite, 0),
                output_tokens: nOutput,
                pricing: OPENAI_FALLBACK_PRICING[sModel],
                total_cost_usd: 0
            };
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
