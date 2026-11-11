{
  "name": "retail_master_pipeline",
  "properties": {
    "description": "End-to-end retail ingestion and transformation orchestration",
    "activities": [
      {
        "name": "Copy_Raw_Sales_To_ADLS",
        "type": "Copy",
        "dependsOn": [],
        "typeProperties": {
          "source": {
            "type": "DelimitedTextSource",
            "storeSettings": {
              "type": "FileServerReadSettings",
              "recursive": false,
              "enablePartitionDiscovery": false
            },
            "formatSettings": {
              "type": "DelimitedTextReadSettings",
              "skipLineCount": 0,
              "quoteChar": "\""
            }
          },
          "sink": {
            "type": "DelimitedTextSink",
            "storeSettings": {
              "type": "AzureBlobFSWriteSettings"
            },
            "formatSettings": {
              "type": "DelimitedTextWriteSettings",
              "quoteAllText": true
            }
          },
          "enableStaging": false
        },
        "inputs": [
          {
            "referenceName": "raw_sales_dataset",
            "type": "DatasetReference"
          }
        ],
        "outputs": [
          {
            "referenceName": "bronze_sales_dataset",
            "type": "DatasetReference"
          }
        ]
      },
      {
        "name": "Run_Bronze_Ingestion_Notebook",
        "type": "DatabricksNotebook",
        "dependsOn": [
          {
            "activity": "Copy_Raw_Sales_To_ADLS",
            "dependencyConditions": [
              "Succeeded"
            ]
          }
        ],
        "typeProperties": {
          "notebookPath": "/Workspace/Users/azure_portfolio/01_bronze_ingest",
          "baseParameters": {
            "source_path": "abfss://landing@<storage_account>.dfs.core.windows.net/sales/",
            "bronze_path": "abfss://bronze@<storage_account>.dfs.core.windows.net/sales/",
            "batch_id": "@{pipeline().RunId}"
          }
        }
      },
      {
        "name": "Run_Silver_Transformation_Notebook",
        "type": "DatabricksNotebook",
        "dependsOn": [
          {
            "activity": "Run_Bronze_Ingestion_Notebook",
            "dependencyConditions": [
              "Succeeded"
            ]
          }
        ],
        "typeProperties": {
          "notebookPath": "/Workspace/Users/azure_portfolio/02_silver_transform",
          "baseParameters": {
            "bronze_path": "abfss://bronze@<storage_account>.dfs.core.windows.net/sales/",
            "silver_path": "abfss://silver@<storage_account>.dfs.core.windows.net/sales/",
            "quarantine_path": "abfss://silver@<storage_account>.dfs.core.windows.net/sales_quarantine/"
          }
        }
      },
      {
        "name": "Run_Gold_Model_Notebook",
        "type": "DatabricksNotebook",
        "dependsOn": [
          {
            "activity": "Run_Silver_Transformation_Notebook",
            "dependencyConditions": [
              "Succeeded"
            ]
          }
        ],
        "typeProperties": {
          "notebookPath": "/Workspace/Users/azure_portfolio/03_gold_dimensional_model",
          "baseParameters": {
            "silver_path": "abfss://silver@<storage_account>.dfs.core.windows.net/sales/",
            "gold_path": "abfss://gold@<storage_account>.dfs.core.windows.net/"
          }
        }
      },
      {
        "name": "Run_Data_Quality_Check_Notebook",
        "type": "DatabricksNotebook",
        "dependsOn": [
          {
            "activity": "Run_Gold_Model_Notebook",
            "dependencyConditions": [
              "Succeeded"
            ]
          }
        ],
        "typeProperties": {
          "notebookPath": "/Workspace/Users/azure_portfolio/04_data_quality_checks",
          "baseParameters": {
            "gold_path": "abfss://gold@<storage_account>.dfs.core.windows.net/"
          }
        }
      }
    ],
    "annotations": [],
    "lastModifiedBy": {
      "name": "Azure Portfolio",
      "type": "User"
    },
    "lastModifiedTime": "2026-11-11T00:00:00Z"
  }
}
