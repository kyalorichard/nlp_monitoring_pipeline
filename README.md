
# Social Media Civic Monitoring Pipeline

This project is an end-to-end NLP pipeline for monitoring civic discourse, detecting hate speech, and classifying narratives from social media platforms including Twitter/X, Facebook, and Google News.

## 📊 Features

- **Real-time data ingestion** from Twitter, Facebook, and Google News
- **Natural Language Processing (NLP)**: Sentiment analysis, Named Entity Recognition (NER), Topic modeling, and Narrative classification
- **Dashboarding**: Streamlit-based interactive dashboard for live insights
- **Modular Design**: Easy to extend with new data sources or NLP models

---

## ⚙️ Setup Instructions

### Windows

```bash
# Clone the repo
git clone https://github.com/your-org/nlp-monitoring-pipeline.git
cd nlp-monitoring-pipeline

# Setup environment
conda create -n nlp_env python=3.10
conda activate nlp_env

# Install dependencies
pip install -r requirements.txt
```

### Linux/macOS

```bash
git clone https://github.com/your-org/nlp-monitoring-pipeline.git
cd nlp-monitoring-pipeline

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 📷 Dashboard Screenshot

![Dashboard Screenshot](screenshots/dashboard_main.png)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- [Kyalo Richard](https://github.com/kyalorichard) — Lead Developer & Data Scientist

---

## 🚧 Project Roadmap

- [x] Add Twitter and Google News ingestion
- [x] Implement NLP classification pipeline
- [x] Integrate Facebook scraping
- [x] Build Streamlit dashboard
- [ ] Add multilingual support
- [ ] Automate deployment to cloud (e.g., Heroku, Azure)
- [ ] Extend to Telegram and WhatsApp monitoring

---

## 💡 Acknowledgments

- Hugging Face Transformers
- Streamlit
- Facebook Scraper
- NewsAPI

---

For feedback or collaboration, feel free to open an issue or reach out via email.
