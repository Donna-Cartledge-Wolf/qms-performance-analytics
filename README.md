# Wolf Analytics: QMS Performance & Change Management Analytics

Portfolio project using 100% synthetic data to demonstrate quality systems analytics, performance monitoring, and management-review decision support.

## Focus

- Complaint and investigation aging
- CAPA status, backlog, and effectiveness
- Change management cycle time and follow-up
- Risk prioritization
- Process performance indicators
- Training and cross-training coverage
- Single-point-of-failure risk
- Management-review decision support

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_synthetic_qms_data.py
python src/qms_metrics.py
streamlit run src/qms_dashboard.py
