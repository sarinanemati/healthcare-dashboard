import io
import pandas as pd
import plotly.express as px
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Healthcare Dashboard", layout="wide")


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    # Normalize column names in case the CSV has extra spaces
    df.columns = df.columns.str.strip()

    # Parse dates
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")

    # Create length of stay
    df["Length of Stay"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days

    # Clean billing
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce")

    # Age bands for better analysis
    age_bins = [0, 18, 30, 45, 60, 75, 100]
    age_labels = ["0-18", "19-30", "31-45", "46-60", "61-75", "76+"]
    df["Age Group"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, include_lowest=True)

    return df


def create_pdf_report(filtered_df):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Healthcare Dashboard Report")

    y -= 30
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Total Patients: {len(filtered_df)}")
    y -= 20
    pdf.drawString(
        50, y,
        f"Avg Billing Amount: {filtered_df['Billing Amount'].mean():,.2f}"
        if not filtered_df.empty else "Avg Billing Amount: N/A"
    )
    y -= 20
    pdf.drawString(
        50, y,
        f"Avg Length of Stay: {filtered_df['Length of Stay'].mean():.1f} days"
        if not filtered_df.empty else "Avg Length of Stay: N/A"
    )
    y -= 20
    pdf.drawString(50, y, f"Hospitals: {filtered_df['Hospital'].nunique()}")

    y -= 35
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Sample Filtered Data")

    y -= 20
    pdf.setFont("Helvetica", 9)

    preview_df = filtered_df.head(20).fillna("")
    columns = ["Name", "Gender", "Age", "Medical Condition", "Hospital", "Billing Amount"]

    for _, row in preview_df.iterrows():
        line = " | ".join([str(row[col])[:20] for col in columns if col in preview_df.columns])
        pdf.drawString(50, y, line[:110])
        y -= 15

        if y < 50:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 9)

    pdf.save()
    buffer.seek(0)
    return buffer


st.title("Healthcare Analytical Dashboard")

file_path = st.sidebar.text_input("CSV file path", "healthcare_dataset.csv")
df = load_data(file_path)

st.sidebar.header("Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

condition_filter = st.sidebar.multiselect(
    "Medical Condition",
    options=sorted(df["Medical Condition"].dropna().unique()),
    default=sorted(df["Medical Condition"].dropna().unique())
)

insurance_filter = st.sidebar.multiselect(
    "Insurance Provider",
    options=sorted(df["Insurance Provider"].dropna().unique()),
    default=sorted(df["Insurance Provider"].dropna().unique())
)

admission_filter = st.sidebar.multiselect(
    "Admission Type",
    options=sorted(df["Admission Type"].dropna().unique()),
    default=sorted(df["Admission Type"].dropna().unique())
)

filtered_df = df[
    df["Gender"].isin(gender_filter) &
    df["Medical Condition"].isin(condition_filter) &
    df["Insurance Provider"].isin(insurance_filter) &
    df["Admission Type"].isin(admission_filter)
].copy()

# PDF download button in sidebar
pdf_file = create_pdf_report(filtered_df)
st.sidebar.download_button(
    label="Download PDF",
    data=pdf_file,
    file_name="healthcare_report.pdf",
    mime="application/pdf"
)

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", len(filtered_df))
col2.metric("Avg Billing Amount", f'{filtered_df["Billing Amount"].mean():,.2f}')
col3.metric("Avg Length of Stay", f'{filtered_df["Length of Stay"].mean():.1f} days')
col4.metric("Hospitals", filtered_df["Hospital"].nunique())

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)

with col1:
    avg_billing = (
        filtered_df.groupby("Medical Condition", as_index=False)["Billing Amount"]
        .mean()
        .sort_values("Billing Amount", ascending=False)
    )

    fig_billing = px.bar(
        avg_billing,
        x="Medical Condition",
        y="Billing Amount",
        title="Average Billing Amount by Medical Condition",
        color="Billing Amount",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_billing, use_container_width=True)

with col2:
    admission_dist = (
        filtered_df["Admission Type"]
        .value_counts()
        .reset_index()
    )
    admission_dist.columns = ["Admission Type", "Count"]

    fig_admission = px.pie(
        admission_dist,
        names="Admission Type",
        values="Count",
        title="Admission Type Distribution"
    )
    st.plotly_chart(fig_admission, use_container_width=True)

# Row 2
col1, col2 = st.columns(2)

with col1:
    test_by_age = (
        filtered_df.groupby(["Age Group", "Test Results"], observed=False)
        .size()
        .reset_index(name="Count")
    )

    fig_age_test = px.bar(
        test_by_age,
        x="Age Group",
        y="Count",
        color="Test Results",
        barmode="group",
        title="Test Results by Age Group"
    )
    st.plotly_chart(fig_age_test, use_container_width=True)

with col2:
    test_by_gender = (
        filtered_df.groupby(["Gender", "Test Results"])
        .size()
        .reset_index(name="Count")
    )

    fig_gender_test = px.bar(
        test_by_gender,
        x="Gender",
        y="Count",
        color="Test Results",
        barmode="group",
        title="Test Results by Gender"
    )
    st.plotly_chart(fig_gender_test, use_container_width=True)

# Row 3
col1, col2 = st.columns(2)

with col1:
    hospital_los = (
        filtered_df.groupby("Hospital", as_index=False)["Length of Stay"]
        .mean()
        .sort_values("Length of Stay", ascending=False)
        .head(15)
    )

    fig_los = px.bar(
        hospital_los,
        x="Length of Stay",
        y="Hospital",
        orientation="h",
        title="Average Length of Stay by Hospital (Top 15)",
        color="Length of Stay",
        color_continuous_scale="Teal"
    )
    st.plotly_chart(fig_los, use_container_width=True)

with col2:
    insurance_compare = (
        filtered_df.groupby("Insurance Provider", as_index=False)["Billing Amount"]
        .mean()
        .sort_values("Billing Amount", ascending=False)
    )

    fig_insurance = px.bar(
        insurance_compare,
        x="Insurance Provider",
        y="Billing Amount",
        title="Average Billing Amount by Insurance Provider",
        color="Insurance Provider"
    )
    st.plotly_chart(fig_insurance, use_container_width=True)

st.markdown("---")
st.subheader("Sample Data")
st.dataframe(filtered_df.head(50), use_container_width=True)
