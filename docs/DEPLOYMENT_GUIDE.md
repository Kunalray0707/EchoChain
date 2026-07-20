# EchoChain Production Deployment Guide

## 1. Local Deployment with Docker Compose
To run the containerized pipeline locally:

```bash
# Build & start container environment
docker-compose up --build -d

# View container execution logs
docker-compose logs -f echochain-engine
```

---

## 2. Standalone Python Setup
```bash
# Clone project repository
git clone https://github.com/your-org/EchoChain.git
cd EchoChain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run synthetic data generator
python datasets/generate_datasets.py

# Execute PySpark Medallion Pipeline
python pyspark_pipeline/run_pipeline.py

# Run unit and data quality tests
pytest tests/ -v
```

---

## 3. Databricks Cloud Lakehouse Deployment
1. Import `pyspark_pipeline/` modules into Databricks Repos.
2. Configure a Databricks Job Cluster (Single Node or Multi-Node, Spark 3.5+, DB runtime 14.3 LTS).
3. Set Delta table target location to DBFS / ADLS Gen2 / AWS S3 bucket: `dbfs:/mnt/echochain/gold/`.
4. Connect Power BI Desktop to Databricks SQL Warehouse via native Databricks connector.
