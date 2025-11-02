import os
import requests

# Target folder (adjust if needed)
TARGET_DIR = "goodblue-model/data/raw"
os.makedirs(TARGET_DIR, exist_ok=True)

# URLs and filenames
files = {
    "2025_mckinsey_state_of_ai.pdf": "https://www.mckinsey.com/~/media/mckinsey/business-functions/quantumblack/our-insights/the-state-of-ai/2025/the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf",
    "2025_stanford_ai_index.pdf": "https://hai.stanford.edu/assets/files/hai_ai_index_report_2025.pdf",
    "2025_servicenow_enterprise_ai_maturity.pdf": "https://www.servicenow.com/content/dam/servicenow-assets/public/en-us/doc-type/resource-center/white-paper/wp-enterprise-ai-maturity-index-2025.pdf",
    "2025_openai_ai_in_enterprise.pdf": "https://cdn.openai.com/business-guides-and-resources/ai-in-the-enterprise.pdf",
    "2024_goldmansachs_powering_ai_era.pdf": "https://www.goldmansachs.com/what-we-do/investment-banking/insights/articles/powering-the-ai-era/report.pdf",
    "2025_ceibs_ai_landscape.pdf": "https://repository.ceibs.edu/files/59116885/AI_Industry_landscape_report_2025.pdf",
    "pwc_ai_sizing_the_prize.pdf": "https://www.pwc.com/gx/en/issues/analytics/assets/pwc-ai-analysis-sizing-the-prize-report.pdf",
    "2023_mossadams_ai_trends.pdf": "https://www.mossadams.com/getmedia/2b5c6f15-ba49-4713-9610-400cec25ddb5/ai_industry_trends_report_2023.pdf",
    "2025_wef_ai_in_action.pdf": "https://reports.weforum.org/docs/WEF_AI_in_Action_Beyond_Experimentation_to_Transform_Industry_2025.pdf",
    "2023_us_state_enterprise_ai_strategy.pdf": "https://www.state.gov/wp-content/uploads/2023/11/Department-of-State-Enterprise-Artificial-Intelligence-Strategy.pdf"
}

def download_file(name, url):
    path = os.path.join(TARGET_DIR, name)
    try:
        print(f"⬇️ Downloading {name} ...")
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ Saved to {path}")
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")

if __name__ == "__main__":
    for filename, link in files.items():
        download_file(filename, link)
