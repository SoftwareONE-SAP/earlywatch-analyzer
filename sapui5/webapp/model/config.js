sap.ui.define([], function () {
    "use strict";

    /**
     * Detect the runtime environment.
     * - "local": localhost development
     * - "azure": Azure-hosted deployment using same-origin API calls
     */
    function detectEnvironment() {
        var hostname = window.location.hostname;
        if (hostname === "localhost" || hostname === "127.0.0.1") {
            return "local";
        }
        if (hostname.indexOf("azurewebsites.net") !== -1 || hostname.indexOf("azurecontainerapps.io") !== -1) {
            return "azure";
        }
        // Default to Azure for unknown deployed domains.
        return "azure";
    }

    var environment = detectEnvironment();

    // Base URL depends on environment
    var apiBaseUrl;
    switch (environment) {
        case "local":
            apiBaseUrl = "http://localhost:8001";
            break;
        case "azure":
            // Hosted deployments use same-origin API calls.
            apiBaseUrl = "";
            break;
        default:
            apiBaseUrl = "";
    }

    return {
        environment: environment,
        apiBaseUrl: apiBaseUrl,

        endpoints: {
            listFiles: "/api/files",
            upload: "/api/upload",
            process: "/api/reprocess-ai",
            deleteAnalysis: "/api/delete-analysis",
            getAnalysis: "/api/download/", // + blobName (for .md or .json)
            exportExcel: "/api/export-excel", // Excel export
            chat: "/api/chat"
        },

        getEndpoint: function (key) {
            return this.apiBaseUrl + this.endpoints[key];
        },

        getDownloadUrl: function (blobName) {
            return this.apiBaseUrl + this.endpoints.getAnalysis + blobName;
        }
    };
});
