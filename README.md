## Supply Chain Logistics Analytics and Performance Optimization



### Objective



The objective of this project is to analyze supply chain shipment data to identify operational inefficiencies, customer behavior patterns, delivery performance issues, and data quality gaps. The project enables data-driven decision-making for logistics optimization.



### Dataset Description



The dataset contains order-level shipment information including:



Shipment dates and ports



Carrier and service levels



Shipment weight and quantity



Delivery delay indicators



Customer and branch identifiers



### Methodology



Data Ingestion



Data loaded from PostgreSQL into Python using SQLAlchemy and Pandas.



Feature Engineering



Derived late delivery indicators



Classified shipments as Domestic or International



Aggregated customer, carrier, and branch-level metrics



Analytical Modules



Shipment distribution analysis



Failure rate detection



Outlier detection



Customer segmentation



Churn prediction



Productivity ranking



Data quality checks





#### **Interactive Streamlit dashboard created for business users**



### Key Insights



Certain origin ports handle significantly higher shipment volumes.



International shipments tend to have higher average weights.



Some branches show disproportionately high late delivery counts, indicating last-mile inefficiencies.



A small set of customers contribute high shipment quantities but place fewer orders.



Carrier performance varies significantly, with measurable differences in delivery success rates.



Data quality issues such as missing values and invalid weights were identified.



## Conclusion



This project demonstrates how Python-based analytics combined with interactive dashboards can provide actionable insights into supply chain performance. The modular architecture allows easy extension to predictive models and real-time monitoring systems.



