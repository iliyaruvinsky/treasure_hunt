# Skywind Exception Indicator Creation Workflow

## Part 1: Choose an appropriate SAP entity (e.g. Table / View / ABAP CDS view etc.) to create an Exception Indicator

### Step-by-Step Process

| Step | Component | Status | Description |
|------|-----------|--------|-------------|
| **01** | **Basic Settings** | **Mandatory** | Select the source (e.g., Table, View, CDS View, etc.) upon which you will create an Exception Indicator, which in turn will serve as a source for alerts and reports. |
| **02** | **Selected Fields** | **Mandatory** | Select up to 100 fields from the source which will be used as alert's parameter and/or an output field for alert's notification |
| **03** | **Currency Conversion** | Optional | Select fields representing Amounts. Based on them, create new "Amount" fields converted to the desired currency. |
| **04** | **External Parameters** | Optional | Set the default values for the External Parameters. (e.g. choose a "Reference Date" field for the historical inquiries etc.). |
| **05** | **Key For Delta** | Optional | Define keys for the Delta (incremental) alerting/reporting. |
| **06** | **Documentation** | Optional | Add the desired explanations and documentation about the newly created Exception Indicator. |

---

## Part 2: Create Alerts and Reports based on an Exception Indicator

### Step-by-Step Process

| Step | Component | Status | Description |
|------|-----------|--------|-------------|
| **01** | **Basic Settings** | **Mandatory** | Set a meaningful name for the alert, define running mode, assign severity etc. |
| **02** | **Format** | **Mandatory** | Choose the fields which will construct alert's output. You can arrange output fields in the desired order and edit original field's descriptions. |
| **03** | **Parameters** | Optional | Restrict the data, which will be fetched by an alert, by adding specific parameter values. |
| **04** | **Recipients** | Optional | Alert notifications can be sent to recipients via Email and Text messages (SMS). Assign desired recipients to the alert. |
| **05** | **Conditions** | Optional | *This feature is currently in development* |
| **06** | **Data Masking** | Optional | Data Masking is used to mask sensitive data (e.g. user's personal data). You can mask all or some fields in any alert |
| **07** | **Scheduling** | **Mandatory** | Establish scheduling plan - configure alert's scanning parameters, such as execution frequency, timeframe. Decide if you want to keep the data, collected by an alert. |

---

## Workflow Summary

### Part 1: Exception Indicator Creation
- **2 Mandatory Steps**: Basic Settings, Selected Fields
- **4 Optional Steps**: Currency Conversion, External Parameters, Key For Delta, Documentation

### Part 2: Alert and Report Creation  
- **3 Mandatory Steps**: Basic Settings, Format, Scheduling
- **4 Optional Steps**: Parameters, Recipients, Conditions*, Data Masking

*Note: Conditions feature is currently in development*

---

## Key Features

### Data Sources Supported
- Tables
- Views  
- ABAP CDS Views
- And more SAP entities

### Alert Capabilities
- Up to 100 fields per Exception Indicator
- Currency conversion for amount fields
- Delta (incremental) alerting
- Email and SMS notifications
- Data masking for sensitive information
- Flexible scheduling options

### Output Options
- Customizable field arrangements
- Editable field descriptions
- Parameter-based data filtering
- Historical inquiry support

---

## Contact Information

**Email:** info@skywind.com  
**Website:** www.skywind.com

---

*© Skywind Software Group*