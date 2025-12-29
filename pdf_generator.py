"""
PDF User Guide Generator for AI Bias Auditor v3.0
Generates professional academic-style PDF guides
Author: AI Bias Auditor Team
Date: December 2025
"""

from fpdf import FPDF
from datetime import datetime


class UserGuidePDF(FPDF):
    """Custom PDF class with header and footer."""
    
    def __init__(self, guide_type="short"):
        super().__init__()
        self.guide_type = guide_type
        
    def header(self):
        """Add header to each page."""
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'AI Bias Auditor v3.0 - User Guide', 0, 0, 'C')
        self.ln(5)
        self.set_draw_color(0, 43, 91)  # Navy Blue
        self.line(10, 20, 200, 20)
        self.ln(10)
    
    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d")}', 0, 0, 'R')
    
    def chapter_title(self, title):
        """Add chapter title."""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 43, 91)  # Navy Blue
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def section_title(self, title):
        """Add section title."""
        self.set_font('Arial', 'B', 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(1)
    
    def body_text(self, text):
        """Add body text."""
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(2)
    
    def add_definition(self, term, definition):
        """Add term definition."""
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, term, 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, definition)
        self.ln(2)
    
    def add_bullet(self, text):
        """Add bullet point."""
        self.set_font('Arial', '', 10)
        current_x = self.get_x()
        current_y = self.get_y()
        self.cell(5, 5, '-', 0, 0, 'L')
        self.set_xy(current_x + 7, current_y)
        self.multi_cell(0, 5, text)
        self.ln(1)


def generate_short_guide():
    """Generate short user guide (3-5 pages)."""
    pdf = UserGuidePDF(guide_type="short")
    pdf.add_page()
    
    # Title Page
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(0, 43, 91)
    pdf.ln(30)
    pdf.cell(0, 10, 'AI BIAS AUDITOR v3.0', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 8, 'USER GUIDE - RINGKAS', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, 'Panduan Penggunaan dan Interpretasi Metrics', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 6, 'Audit Teknologi dan Sistem Informasi', 0, 1, 'C')
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    
    # Page 2: Glossary
    pdf.add_page()
    pdf.chapter_title('1. GLOSSARY - DEFINISI ISTILAH')
    
    pdf.add_definition(
        'Approval Rate',
        'Persentase applicants yang disetujui (loan approved) dari total applicants dalam suatu kelompok. '
        'Formula: (Jumlah Approved / Total Applicants) x 100%. '
        'Contoh: Jika 72 dari 100 applicants disetujui, approval rate = 72%.'
    )
    
    pdf.add_definition(
        'Credit Score',
        'Nilai numerik (skala 300-850) yang merepresentasikan kelayakan kredit seseorang. '
        'Semakin tinggi skor, semakin rendah risiko gagal bayar. '
        'Kategori: 300-500 (High Risk), 500-600 (Medium Risk), 600-700 (Low Risk), 700-850 (Very Low Risk).'
    )
    
    pdf.add_definition(
        'Age Group',
        'Klasifikasi applicants berdasarkan umur: Young (<=45 tahun) dan Old (>45 tahun). '
        'Threshold 45 tahun digunakan untuk mendeteksi age discrimination (ageism).'
    )
    
    pdf.add_definition(
        'Bias (Bias Sistemik)',
        'Perlakuan tidak adil secara sistematis terhadap kelompok tertentu dalam proses pengambilan keputusan AI. '
        'Dalam konteks ini: diskriminasi berdasarkan umur (age discrimination).'
    )
    
    pdf.add_definition(
        'Disparate Impact (DI) Ratio',
        'Rasio approval rate kelompok minoritas dibanding kelompok mayoritas. '
        'Formula: (Approval Rate Old / Approval Rate Young). '
        'Standard legal: DI Ratio >= 0.80 (80% Rule dari EEOC). '
        'Jika < 0.80, indikasi diskriminasi yang dapat digugat secara hukum.'
    )
    
    pdf.add_definition(
        'p-value',
        'Probabilitas bahwa perbedaan yang diamati terjadi karena kebetulan (random chance). '
        'Interpretasi: p < 0.05 = perbedaan signifikan secara statistik (bukan kebetulan). '
        'p < 0.01 = sangat signifikan. p > 0.05 = tidak ada perbedaan yang signifikan.'
    )
    
    # Page 3: Statistical Metrics
    pdf.add_page()
    pdf.chapter_title('2. CARA BACA METRICS')
    
    pdf.section_title('2.1. Score Gap (Selisih Skor)')
    pdf.body_text(
        'Perbedaan rata-rata credit score antara kelompok Young dan Old. '
        'Formula: Avg Score Young - Avg Score Old.\n\n'
        'Interpretasi:\n'
        '- Gap < 50 points: Perbedaan kecil, mungkin wajar\n'
        '- Gap 50-100 points: Perbedaan moderat, perlu investigasi\n'
        '- Gap > 100 points: Perbedaan besar, indikasi BIAS KUAT\n\n'
        'Contoh: Jika Young avg = 632 dan Old avg = 439, maka Gap = 193 points (BIAS!).'
    )
    
    pdf.section_title('2.2. Approval Gap (Selisih Approval Rate)')
    pdf.body_text(
        'Perbedaan approval rate antara kelompok Young dan Old. '
        'Formula: Approval Rate Young - Approval Rate Old.\n\n'
        'Interpretasi:\n'
        '- Gap < 10%: Perbedaan kecil, relatif fair\n'
        '- Gap 10-20%: Perbedaan moderat, perlu monitoring\n'
        '- Gap > 20%: Perbedaan besar, indikasi BIAS\n\n'
        'Contoh: Jika Young = 72.4% dan Old = 28.6%, maka Gap = 43.8% (BIAS SIGNIFIKAN!).'
    )
    
    pdf.section_title('2.3. T-Test dan Mann-Whitney U Test')
    pdf.body_text(
        'Statistical tests untuk menguji apakah perbedaan antara 2 kelompok signifikan.\n\n'
        'T-Test: Parametric test (asumsi distribusi normal)\n'
        'Mann-Whitney U: Non-parametric test (tidak asumsi distribusi)\n\n'
        'Cara Baca p-value:\n'
        '- p < 0.001: Extremely significant (99.9% confidence)\n'
        '- p < 0.01: Highly significant (99% confidence)\n'
        '- p < 0.05: Significant (95% confidence) - THRESHOLD STANDARD\n'
        '- p >= 0.05: Not significant (no strong evidence of difference)\n\n'
        'Contoh: p-value = 0.00000001 artinya perbedaan SANGAT SIGNIFIKAN, bukan kebetulan.'
    )
    
    pdf.add_page()
    pdf.section_title('2.4. Cohen\'s d (Effect Size)')
    pdf.body_text(
        'Ukuran seberapa BESAR perbedaan antara 2 kelompok, independent dari sample size. '
        'Formula: (Mean1 - Mean2) / Pooled Standard Deviation.\n\n'
        'Interpretasi (Cohen, 1988):\n'
        '- d = 0.2: Small effect (perbedaan kecil)\n'
        '- d = 0.5: Medium effect (perbedaan sedang)\n'
        '- d = 0.8: Large effect (perbedaan besar)\n'
        '- d > 1.0: Very large effect (perbedaan sangat besar)\n\n'
        'Contoh: Cohen\'s d = 3.142 artinya LARGE EFFECT, bias sangat besar dan praktis signifikan.'
    )
    
    pdf.section_title('2.5. Disparate Impact Ratio (80% Rule)')
    pdf.body_text(
        'Legal standard dari EEOC (Equal Employment Opportunity Commission) untuk mendeteksi diskriminasi.\n\n'
        'Formula: (Selection Rate Minoritas / Selection Rate Mayoritas)\n\n'
        'Standard Legal:\n'
        '- DI >= 0.80: PASS (Compliant, fair)\n'
        '- DI < 0.80: FAIL (Non-compliant, potential legal violation)\n'
        '- DI < 0.50: Severe violation (highly discriminatory)\n\n'
        'Contoh: DI = 0.394 artinya Old group hanya 39.4% kemungkinan approved dibanding Young group. '
        'Ini FAIL karena < 0.80, indikasi DISKRIMINASI yang dapat digugat.'
    )
    
    # Page 4: Interpretation Guide
    pdf.add_page()
    pdf.chapter_title('3. INTERPRETASI HASIL AUDIT')
    
    pdf.section_title('3.1. Kapan Bias Terdeteksi?')
    pdf.body_text(
        'Bias dinyatakan TERDETEKSI jika memenuhi SALAH SATU kriteria berikut:\n'
    )
    pdf.add_bullet('Score Gap > 100 points')
    pdf.add_bullet('Approval Gap > 20%')
    pdf.add_bullet('Disparate Impact Ratio < 0.80')
    pdf.add_bullet('T-Test p-value < 0.05 (signifikan)')
    pdf.add_bullet('Cohen\'s d > 0.8 (large effect)')
    pdf.ln(3)
    
    pdf.body_text(
        'Jika SEMUA kriteria terpenuhi: BIAS KUAT dan JELAS (immediate action required).'
    )
    
    pdf.section_title('3.2. Level Severity (Tingkat Keparahan)')
    pdf.body_text(
        'LOW SEVERITY:\n'
        '- Score Gap: 50-100 points\n'
        '- Approval Gap: 10-20%\n'
        '- DI Ratio: 0.70-0.79\n'
        '- Rekomendasi: Monitoring dan minor adjustment\n\n'
        'MEDIUM SEVERITY:\n'
        '- Score Gap: 100-150 points\n'
        '- Approval Gap: 20-30%\n'
        '- DI Ratio: 0.50-0.69\n'
        '- Rekomendasi: Model review dan fairness intervention\n\n'
        'HIGH SEVERITY:\n'
        '- Score Gap: > 150 points\n'
        '- Approval Gap: > 30%\n'
        '- DI Ratio: < 0.50\n'
        '- Rekomendasi: Immediate model redesign, legal review'
    )
    
    pdf.section_title('3.3. Compliance Status')
    pdf.body_text(
        'COMPLIANT: DI Ratio >= 0.80, no significant bias detected, meets fairness criteria.\n\n'
        'NON-COMPLIANT: DI Ratio < 0.80, significant bias detected, violates 80% Rule.\n'
        '- Risk: Legal liability, regulatory fines, reputational damage\n'
        '- Action: Immediate intervention required'
    )
    
    # Page 5: References
    pdf.add_page()
    pdf.chapter_title('4. REFERENSI & TINJAUAN PUSTAKA')
    
    pdf.section_title('4.1. Legal & Regulatory Standards')
    pdf.add_bullet('EEOC (1978). Uniform Guidelines on Employee Selection Procedures. 80% Rule for Disparate Impact.')
    pdf.add_bullet('UU No. 8/1999 tentang Perlindungan Konsumen (Indonesia).')
    pdf.add_bullet('OJK Regulation on Financial Services Consumer Protection.')
    pdf.add_bullet('ISO/IEC 24027:2021 - Bias in AI systems and AI aided decisions.')
    pdf.ln(3)
    
    pdf.section_title('4.2. Academic References')
    pdf.add_bullet('Barocas, S., & Selbst, A. D. (2016). Big Data\'s Disparate Impact. California Law Review, 104, 671.')
    pdf.add_bullet('Feldman, M., et al. (2015). Certifying and Removing Disparate Impact. ACM SIGKDD.')
    pdf.add_bullet('Mehrabi, N., et al. (2021). A Survey on Bias and Fairness in Machine Learning. ACM Computing Surveys.')
    pdf.add_bullet('Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.).')
    pdf.ln(3)
    
    pdf.section_title('4.3. Tools & Libraries')
    pdf.add_bullet('Streamlit 1.32+ - Interactive web dashboard framework')
    pdf.add_bullet('Pandas 2.2+ - Data manipulation and analysis')
    pdf.add_bullet('SciPy 1.11+ - Statistical computing and hypothesis testing')
    pdf.add_bullet('Plotly 5.19+ - Interactive data visualization')
    pdf.add_bullet('Scikit-learn 1.7+ - Machine learning metrics and evaluation')
    
    return pdf


def generate_full_guide():
    """Generate comprehensive user guide (10-15 pages)."""
    pdf = UserGuidePDF(guide_type="full")
    pdf.add_page()
    
    # Title Page
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(0, 43, 91)
    pdf.ln(30)
    pdf.cell(0, 10, 'AI BIAS AUDITOR v3.0', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 8, 'USER GUIDE - COMPREHENSIVE', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, 'Panduan Lengkap Penggunaan, Interpretasi, dan Metodologi', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 6, 'Audit Teknologi dan Sistem Informasi', 0, 1, 'C')
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    
    # All content from short guide
    pdf.add_page()
    pdf.chapter_title('1. PENGENALAN AI BIAS AUDITOR')
    
    pdf.section_title('1.1. Latar Belakang')
    pdf.body_text(
        'AI Bias Auditor v3.0 adalah tool profesional untuk mendeteksi dan mengukur bias sistemik '
        'dalam sistem credit scoring berbasis AI. Tool ini dirancang untuk membantu auditor, '
        'data scientist, compliance officer, dan stakeholder terkait dalam:\n'
    )
    pdf.add_bullet('Mengidentifikasi diskriminasi berdasarkan umur (age discrimination)')
    pdf.add_bullet('Mengukur disparate impact dengan metode statistik yang robust')
    pdf.add_bullet('Memvisualisasikan pola bias dengan 18+ interactive charts')
    pdf.add_bullet('Memberikan rekomendasi actionable untuk fairness intervention')
    pdf.add_bullet('Memastikan compliance dengan regulasi (EEOC, OJK, ISO 24027)')
    pdf.ln(3)
    
    pdf.section_title('1.2. Fitur Utama')
    pdf.add_bullet('18+ Interactive Visualizations (Heatmap, Violin Plot, Sunburst, Radar Chart)')
    pdf.add_bullet('8 Statistical Tests (T-Test, Mann-Whitney U, Cohen\'s d, DI Ratio, dll)')
    pdf.add_bullet('6 ML Fairness Metrics (DPD, EOD, Predictive Parity)')
    pdf.add_bullet('Real-time Progress Tracking')
    pdf.add_bullet('Multiple Export Formats (CSV, TXT, JSON)')
    pdf.add_bullet('Professional Academic Documentation')
    pdf.ln(5)
    
    # Chapter 2: Glossary (Extended)
    pdf.add_page()
    pdf.chapter_title('2. GLOSSARY - DEFINISI ISTILAH LENGKAP')
    
    pdf.add_definition(
        'Applicant',
        'Individu yang mengajukan permohonan kredit/pinjaman kepada lembaga keuangan. '
        'Dalam dataset, setiap applicant memiliki ID unik dan atribut seperti Age, Income, Credit Score.'
    )
    
    pdf.add_definition(
        'Approval Rate',
        'Persentase applicants yang disetujui (loan approved) dari total applicants dalam suatu kelompok. '
        'Formula: (Jumlah Approved / Total Applicants) x 100%. '
        'Contoh: Jika 72 dari 100 applicants disetujui, approval rate = 72%. '
        'Metric ini digunakan untuk membandingkan treatment antara kelompok Young dan Old.'
    )
    
    pdf.add_definition(
        'Credit Score',
        'Nilai numerik (skala 300-850) yang merepresentasikan kelayakan kredit seseorang berdasarkan '
        'berbagai faktor seperti payment history, income, debt-to-income ratio, credit history length, dll. '
        'Semakin tinggi skor, semakin rendah risiko gagal bayar. '
        'Kategori standard: 300-500 (High Risk), 500-600 (Medium Risk), 600-700 (Low Risk), 700-850 (Very Low Risk). '
        'Threshold approval biasanya di 600 (applicants dengan score >= 600 disetujui).'
    )
    
    pdf.add_definition(
        'Age Group',
        'Klasifikasi applicants berdasarkan umur untuk analisis bias: '
        'Young (umur <= 45 tahun) dan Old (umur > 45 tahun). '
        'Threshold 45 tahun dipilih berdasarkan Age Discrimination in Employment Act (ADEA) '
        'yang melindungi workers berumur 40+ tahun. Dalam credit scoring, threshold ini digunakan '
        'untuk mendeteksi age discrimination (ageism).'
    )
    
    pdf.add_definition(
        'Bias (Bias Sistemik)',
        'Perlakuan tidak adil secara sistematis terhadap kelompok tertentu (protected group) '
        'dalam proses pengambilan keputusan AI. Bias dapat terjadi karena: (1) Data bias (historical discrimination), '
        '(2) Algorithm bias (flawed model design), (3) Proxy discrimination (fitur yang berkorelasi dengan protected attribute). '
        'Dalam konteks ini: diskriminasi berdasarkan umur (age discrimination / ageism).'
    )
    
    pdf.add_page()
    pdf.add_definition(
        'Disparate Impact (DI) Ratio',
        'Rasio selection rate (approval rate) kelompok minoritas/protected dibanding kelompok mayoritas. '
        'Formula: (Selection Rate Minoritas / Selection Rate Mayoritas). '
        'Dalam konteks ini: (Approval Rate Old / Approval Rate Young). '
        'Standard legal: DI Ratio >= 0.80 (80% Rule dari EEOC Uniform Guidelines 1978). '
        'Jika DI < 0.80, indikasi adverse impact yang dapat digugat secara hukum. '
        'Contoh: Jika Young approval = 72% dan Old approval = 29%, DI = 29/72 = 0.40 (FAIL!).'
    )
    
    pdf.add_definition(
        'p-value',
        'Probabilitas bahwa perbedaan yang diamati terjadi karena kebetulan (random chance) jika null hypothesis benar. '
        'Null hypothesis: Tidak ada perbedaan antara kelompok Young dan Old. '
        'Interpretasi: p < 0.05 = perbedaan signifikan secara statistik (reject null hypothesis, bukan kebetulan). '
        'p < 0.01 = sangat signifikan. p < 0.001 = extremely significant. '
        'p >= 0.05 = tidak ada perbedaan yang signifikan (fail to reject null hypothesis). '
        'Threshold standard: alpha = 0.05 (95% confidence level).'
    )
    
    pdf.add_definition(
        'T-Test (Independent Samples T-Test)',
        'Parametric statistical test untuk membandingkan mean (rata-rata) dari 2 independent groups. '
        'Asumsi: (1) Data berdistribusi normal, (2) Equal/unequal variance. '
        'Menghasilkan: t-statistic dan p-value. '
        'Digunakan untuk menguji apakah perbedaan rata-rata credit score antara Young dan Old signifikan.'
    )
    
    pdf.add_definition(
        'Mann-Whitney U Test',
        'Non-parametric statistical test (distribution-free) untuk membandingkan 2 independent groups. '
        'Alternatif T-Test yang tidak mengasumsikan distribusi normal. '
        'Lebih robust terhadap outliers dan skewed distributions. '
        'Menghasilkan: U-statistic dan p-value. '
        'Interpretasi p-value sama dengan T-Test.'
    )
    
    pdf.add_definition(
        'Cohen\'s d (Effect Size)',
        'Ukuran standardized untuk seberapa BESAR perbedaan antara 2 kelompok, independent dari sample size. '
        'Formula: (Mean1 - Mean2) / Pooled Standard Deviation. '
        'Interpretasi (Cohen, 1988): d = 0.2 (small), d = 0.5 (medium), d = 0.8 (large), d > 1.0 (very large). '
        'Contoh: d = 3.142 artinya perbedaan 3.14 standard deviations, extremely large effect.'
    )
    
    pdf.add_page()
    pdf.add_definition(
        'Demographic Parity Difference (DPD)',
        'Selisih selection rate antara 2 kelompok. Formula: Selection Rate Group A - Selection Rate Group B. '
        'Idealnya DPD = 0 (perfect parity). DPD > 20% indikasi bias signifikan. '
        'Merupakan ML fairness metric untuk demographic parity / statistical parity.'
    )
    
    pdf.add_definition(
        'Equal Opportunity Difference (EOD)',
        'Selisih True Positive Rate (TPR) antara 2 kelompok. TPR = Sensitivity = Recall. '
        'Formula: TPR Group A - TPR Group B. '
        'Fokus pada fairness untuk "qualified individuals" (yang seharusnya approved). '
        'Idealnya EOD = 0. Metric ini lebih strict dari Demographic Parity.'
    )
    
    pdf.add_definition(
        'Predictive Parity',
        'Rasio Positive Predictive Value (PPV) antara 2 kelompok. PPV = Precision. '
        'Formula: PPV Group A / PPV Group B. '
        'Fokus pada fairness untuk "predicted positives". '
        'Idealnya ratio = 1.0 (equal precision across groups).'
    )
    
    pdf.add_definition(
        'Proxy Discrimination',
        'Diskriminasi tidak langsung melalui fitur yang berkorelasi tinggi dengan protected attribute. '
        'Contoh: Employment_Years berkorelasi dengan Age (orang tua = lama kerja). '
        'Jika model memberikan bobot tinggi pada Employment_Years, efektifnya sama dengan diskriminasi Age. '
        'Deteksi: Correlation Heatmap untuk identifikasi proxy features.'
    )
    
    # Chapter 3: How to Read Metrics (Extended)
    pdf.add_page()
    pdf.chapter_title('3. CARA BACA METRICS LENGKAP')
    
    pdf.section_title('3.1. Executive Summary Metrics')
    pdf.body_text(
        'Executive Summary menampilkan 5 Key Performance Indicators (KPI) di bagian atas dashboard:\n'
    )
    
    pdf.body_text(
        '1. Total Applicants: Jumlah total applicants dalam dataset.\n'
        '   - Interpretasi: Semakin besar sample, semakin reliable hasil statistik.\n'
        '   - Minimum recommended: 100 applicants (30 per group).\n\n'
        '2. Young (<=45): Jumlah applicants muda + approval rate mereka.\n'
        '   - Delta indicator: Persentase yang approved.\n'
        '   - Contoh: 580 applicants, 72.4% approved.\n\n'
        '3. Old (>45): Jumlah applicants tua + approval rate mereka.\n'
        '   - Delta indicator: Persentase yang approved.\n'
        '   - Contoh: 420 applicants, 28.6% approved.\n\n'
        '4. Bias Status: Indikator utama apakah bias terdeteksi.\n'
        '   - [!] DETECTED: Ada bias signifikan (action required).\n'
        '   - [OK] NOT DETECTED: Tidak ada bias signifikan (monitoring).\n'
        '   - Delta: Approval gap percentage.\n\n'
        '5. 80% Rule: Compliance dengan Disparate Impact standard.\n'
        '   - PASS: DI Ratio >= 0.80 (compliant).\n'
        '   - FAIL: DI Ratio < 0.80 (non-compliant, legal risk).\n'
        '   - Value: Actual DI Ratio.\n'
    )
    
    pdf.add_page()
    pdf.section_title('3.2. Score Gap (Selisih Skor) - Detail')
    pdf.body_text(
        'Score Gap mengukur perbedaan rata-rata credit score antara kelompok Young dan Old.\n\n'
        'Formula:\n'
        'Score Gap = Average Credit Score (Young) - Average Credit Score (Old)\n\n'
        'Interpretasi Berdasarkan Magnitude:\n'
        '- Gap < 25 points: Perbedaan trivial, likely random variation\n'
        '- Gap 25-50 points: Perbedaan kecil, mungkin wajar tergantung konteks\n'
        '- Gap 50-100 points: Perbedaan moderat, perlu investigasi lebih lanjut\n'
        '- Gap 100-150 points: Perbedaan besar, strong indicator of bias\n'
        '- Gap > 150 points: Perbedaan sangat besar, clear evidence of systematic discrimination\n\n'
        'Contoh Perhitungan:\n'
        'Average Score Young = 632 points\n'
        'Average Score Old = 439 points\n'
        'Score Gap = 632 - 439 = 193 points\n'
        'Interpretasi: Gap 193 points adalah BESAR (>150), clear evidence of age bias.\n\n'
        'Catatan:\n'
        '- Gap positif: Young lebih tinggi (discrimination against Old)\n'
        '- Gap negatif: Old lebih tinggi (discrimination against Young, rare case)\n'
        '- Threshold 100 points dipilih berdasarkan praktik industri dan fairness research.'
    )
    
    pdf.add_page()
    pdf.section_title('3.3. Approval Gap (Selisih Approval Rate) - Detail')
    pdf.body_text(
        'Approval Gap mengukur perbedaan approval rate antara kelompok Young dan Old.\n\n'
        'Formula:\n'
        'Approval Gap = Approval Rate (Young) - Approval Rate (Old)\n\n'
        'Interpretasi Berdasarkan Magnitude:\n'
        '- Gap < 5%: Perbedaan trivial, acceptable variation\n'
        '- Gap 5-10%: Perbedaan kecil, relatif fair, monitoring recommended\n'
        '- Gap 10-20%: Perbedaan moderat, perlu investigation dan possible intervention\n'
        '- Gap 20-30%: Perbedaan besar, strong evidence of disparate treatment\n'
        '- Gap > 30%: Perbedaan sangat besar, severe discrimination, immediate action required\n\n'
        'Contoh Perhitungan:\n'
        'Approval Rate Young = 72.4%\n'
        'Approval Rate Old = 28.6%\n'
        'Approval Gap = 72.4% - 28.6% = 43.8%\n'
        'Interpretasi: Gap 43.8% adalah SANGAT BESAR (>30%), severe age discrimination.\n\n'
        'Hubungan dengan Disparate Impact:\n'
        'Approval Gap dan DI Ratio saling terkait:\n'
        '- Jika Approval Gap besar, DI Ratio akan kecil (< 0.80)\n'
        '- Jika Approval Gap kecil, DI Ratio akan mendekati 1.0\n'
        'Contoh: Gap 43.8% -> DI = 28.6/72.4 = 0.395 (FAIL)\n\n'
        'Threshold 20% dipilih berdasarkan fairness literature dan praktik audit.'
    )
    
    pdf.add_page()
    pdf.section_title('3.4. T-Test dan p-value - Detail')
    pdf.body_text(
        'T-Test menguji null hypothesis: "Tidak ada perbedaan mean antara Young dan Old".\n\n'
        'Output T-Test:\n'
        '1. t-statistic: Ukuran seberapa jauh sample mean dari null hypothesis.\n'
        '   - t besar (>2 atau <-2): Strong evidence against null hypothesis\n'
        '   - t kecil (-2 to 2): Weak evidence\n\n'
        '2. p-value: Probabilitas mendapatkan hasil ini jika null hypothesis benar.\n'
        '   - p < 0.001: Extremely significant (***) - 99.9% confidence\n'
        '   - p < 0.01: Highly significant (**) - 99% confidence\n'
        '   - p < 0.05: Significant (*) - 95% confidence - THRESHOLD STANDARD\n'
        '   - p >= 0.05: Not significant (ns) - fail to reject null hypothesis\n\n'
        'Interpretasi p-value:\n'
        'p = 0.00000001 artinya:\n'
        '- Probabilitas hasil ini terjadi secara kebetulan: 0.000001%\n'
        '- Confidence bahwa perbedaan REAL: 99.999999%\n'
        '- Conclusion: REJECT null hypothesis, perbedaan SIGNIFIKAN\n\n'
        'Catatan Penting:\n'
        '- p-value menunjukkan SIGNIFIKANSI, bukan MAGNITUDE\n'
        '- p-value kecil + small effect size = signifikan tapi tidak praktis penting\n'
        '- p-value kecil + large effect size = signifikan DAN praktis penting\n'
        '- Selalu kombinasikan p-value dengan effect size (Cohen\'s d)\n\n'
        'Asumsi T-Test:\n'
        '1. Independent samples (Young dan Old tidak overlap)\n'
        '2. Normal distribution (dapat direlaksasi dengan sample besar, n>30)\n'
        '3. Homogeneity of variance (dapat gunakan Welch\'s t-test jika tidak terpenuhi)'
    )
    
    pdf.add_page()
    pdf.section_title('3.5. Mann-Whitney U Test - Detail')
    pdf.body_text(
        'Mann-Whitney U Test adalah alternatif non-parametric untuk T-Test.\n\n'
        'Kapan Digunakan:\n'
        '- Data tidak berdistribusi normal (skewed, heavy-tailed)\n'
        '- Ada outliers yang ekstrem\n'
        '- Sample size kecil (n < 30)\n'
        '- Data ordinal (bukan interval/ratio)\n\n'
        'Cara Kerja:\n'
        'Test ini membandingkan RANK (peringkat) data, bukan nilai actual.\n'
        '- Rank semua data dari terendah ke tertinggi\n'
        '- Bandingkan sum of ranks antara 2 kelompok\n'
        '- Hitung U-statistic\n\n'
        'Output:\n'
        '1. U-statistic: Ukuran perbedaan rank sum\n'
        '2. p-value: Interpretasi sama dengan T-Test\n\n'
        'Keuntungan:\n'
        '- Lebih robust terhadap outliers\n'
        '- Tidak asumsi distribusi\n'
        '- Lebih conservative (less likely false positive)\n\n'
        'Kekurangan:\n'
        '- Less powerful dibanding T-Test (jika data memang normal)\n'
        '- Lebih sulit interpretasi (rank-based)\n\n'
        'Rekomendasi:\n'
        'Gunakan KEDUANYA (T-Test DAN Mann-Whitney U):\n'
        '- Jika KEDUANYA signifikan: Strong evidence\n'
        '- Jika hanya salah satu signifikan: Investigate further\n'
        '- Jika KEDUANYA tidak signifikan: No evidence of bias'
    )
    
    pdf.add_page()
    pdf.section_title('3.6. Cohen\'s d (Effect Size) - Detail')
    pdf.body_text(
        'Cohen\'s d mengukur MAGNITUDE of difference antara 2 kelompok.\n\n'
        'Formula:\n'
        'd = (Mean1 - Mean2) / Pooled Standard Deviation\n'
        'Pooled SD = sqrt(((n1-1)*SD1^2 + (n2-1)*SD2^2) / (n1+n2-2))\n\n'
        'Interpretasi (Cohen, 1988):\n'
        'd = 0.0 - 0.2: Trivial/Negligible effect\n'
        'd = 0.2 - 0.5: Small effect\n'
        'd = 0.5 - 0.8: Medium effect\n'
        'd = 0.8 - 1.2: Large effect\n'
        'd > 1.2: Very large effect\n'
        'd > 2.0: Huge effect (extremely rare in social sciences)\n\n'
        'Contoh:\n'
        'd = 3.142 artinya:\n'
        '- Perbedaan mean = 3.14 standard deviations\n'
        '- Extremely large effect (jauh di atas threshold 0.8)\n'
        '- Praktis signifikan: Perbedaan terlihat jelas dalam praktik\n\n'
        'Keuntungan Cohen\'s d:\n'
        '- Independent dari sample size (berbeda dengan p-value)\n'
        '- Ukuran practical significance, bukan statistical significance\n'
        '- Dapat dibandingkan across studies\n'
        '- Interpretasi lebih intuitif\n\n'
        'Kombinasi p-value dan Cohen\'s d:\n'
        '- p < 0.05 + d < 0.2: Signifikan tapi tidak praktis penting\n'
        '- p < 0.05 + d > 0.8: Signifikan DAN praktis penting (ACTION REQUIRED)\n'
        '- p > 0.05 + d > 0.8: Tidak signifikan, mungkin sample size kecil\n'
        '- p > 0.05 + d < 0.2: Tidak signifikan dan tidak penting'
    )
    
    pdf.add_page()
    pdf.section_title('3.7. Disparate Impact Ratio (80% Rule) - Detail')
    pdf.body_text(
        'Disparate Impact Ratio adalah legal standard untuk mendeteksi discrimination.\n\n'
        'Sejarah:\n'
        'EEOC Uniform Guidelines on Employee Selection Procedures (1978) menetapkan "Four-Fifths Rule" atau "80% Rule" '
        'sebagai threshold untuk adverse impact dalam employment selection.\n\n'
        'Formula:\n'
        'DI Ratio = (Selection Rate Protected Group / Selection Rate Reference Group)\n'
        'Dalam konteks ini: DI = (Approval Rate Old / Approval Rate Young)\n\n'
        'Legal Standard:\n'
        '- DI >= 0.80: PASS (Presumption of no adverse impact)\n'
        '- DI < 0.80: FAIL (Adverse impact, potential legal violation)\n'
        '- DI < 0.50: Severe adverse impact (high legal risk)\n\n'
        'Contoh Perhitungan:\n'
        'Approval Rate Young = 72.4%\n'
        'Approval Rate Old = 28.6%\n'
        'DI Ratio = 28.6 / 72.4 = 0.395\n'
        'Interpretation: 0.395 < 0.80 -> FAIL\n'
        'Artinya: Old group hanya 39.5% sebesar kemungkinan Young group untuk approved.\n'
        'Ini di bawah 80% threshold, indikasi adverse impact yang dapat digugat.\n\n'
        'Legal Implications:\n'
        '- DI < 0.80: Prima facie evidence of discrimination (burden of proof shifts to defendant)\n'
        '- Defendant harus membuktikan: (1) Business necessity, (2) Job-related, (3) No less discriminatory alternative\n'
        '- Jika gagal membuktikan: Liable for discrimination (fines, damages, corrective action)\n\n'
        'Aplikasi di Credit Scoring:\n'
        'Meskipun 80% Rule berasal dari employment law, prinsip yang sama applicable untuk:\n'
        '- Fair lending practices\n'
        '- Consumer protection law\n'
        '- AI ethics and fairness standards (ISO 24027)\n'
        '- Corporate governance and ESG (Environmental, Social, Governance)'
    )
    
    # Chapter 4: Interpretation Examples
    pdf.add_page()
    pdf.chapter_title('4. CONTOH INTERPRETASI LENGKAP')
    
    pdf.section_title('4.1. Skenario 1: Bias Terdeteksi (High Severity)')
    pdf.body_text(
        'Dataset: 1000 applicants (580 Young, 420 Old)\n\n'
        'Metrics:\n'
        '- Young Approval Rate: 72.4%\n'
        '- Old Approval Rate: 28.6%\n'
        '- Approval Gap: 43.8%\n'
        '- Young Avg Score: 632\n'
        '- Old Avg Score: 439\n'
        '- Score Gap: 193 points\n'
        '- DI Ratio: 0.395\n'
        '- T-Test p-value: 0.00000001\n'
        '- Cohen\'s d: 3.142\n\n'
        'Interpretasi:\n'
        '1. Approval Gap 43.8% >> 20% threshold -> BIAS SIGNIFIKAN\n'
        '2. Score Gap 193 points >> 100 threshold -> BIAS SIGNIFIKAN\n'
        '3. DI Ratio 0.395 << 0.80 -> FAIL 80% Rule, LEGAL VIOLATION\n'
        '4. p-value 0.00000001 << 0.05 -> EXTREMELY SIGNIFICANT\n'
        '5. Cohen\'s d 3.142 >> 0.8 -> VERY LARGE EFFECT\n\n'
        'Kesimpulan:\n'
        'SEVERE AGE DISCRIMINATION DETECTED. Semua metrics menunjukkan bias yang jelas dan signifikan. '
        'System memberikan treatment yang sangat berbeda terhadap applicants berumur >45 tahun. '
        'DI Ratio jauh di bawah 80% threshold, mengindikasikan adverse impact yang melanggar hukum.\n\n'
        'Severity Level: HIGH (Immediate action required)\n\n'
        'Rekomendasi:\n'
        '1. Immediate: Suspend penggunaan model untuk approval decisions\n'
        '2. Investigation: Audit model logic, identifikasi source of bias\n'
        '3. Legal review: Konsultasi legal team terkait compliance risk\n'
        '4. Remediation: Retrain model dengan fairness constraints\n'
        '5. Monitoring: Deploy continuous bias monitoring dashboard\n'
        '6. Transparency: Disclose bias findings ke stakeholders\n'
        '7. Compensation: Review past decisions, possible remediation untuk affected applicants'
    )
    
    pdf.add_page()
    pdf.section_title('4.2. Skenario 2: Bias Tidak Terdeteksi (Fair System)')
    pdf.body_text(
        'Dataset: 1000 applicants (520 Young, 480 Old)\n\n'
        'Metrics:\n'
        '- Young Approval Rate: 65.2%\n'
        '- Old Approval Rate: 62.8%\n'
        '- Approval Gap: 2.4%\n'
        '- Young Avg Score: 615\n'
        '- Old Avg Score: 608\n'
        '- Score Gap: 7 points\n'
        '- DI Ratio: 0.963\n'
        '- T-Test p-value: 0.234\n'
        '- Cohen\'s d: 0.08\n\n'
        'Interpretasi:\n'
        '1. Approval Gap 2.4% << 20% threshold -> NO SIGNIFICANT BIAS\n'
        '2. Score Gap 7 points << 100 threshold -> NO SIGNIFICANT BIAS\n'
        '3. DI Ratio 0.963 >> 0.80 -> PASS 80% Rule, COMPLIANT\n'
        '4. p-value 0.234 >> 0.05 -> NOT SIGNIFICANT\n'
        '5. Cohen\'s d 0.08 << 0.8 -> NEGLIGIBLE EFFECT\n\n'
        'Kesimpulan:\n'
        'NO BIAS DETECTED. System menunjukkan treatment yang fair dan equitable terhadap kedua age groups. '
        'Perbedaan approval rate dan credit score sangat kecil dan tidak signifikan secara statistik. '
        'DI Ratio di atas 80% threshold, mengindikasikan compliance dengan fairness standards.\n\n'
        'Severity Level: NONE (System is fair)\n\n'
        'Rekomendasi:\n'
        '1. Continue monitoring: Maintain bias monitoring sebagai best practice\n'
        '2. Documentation: Document fairness findings untuk audit trail\n'
        '3. Periodic review: Re-audit setiap quarter atau saat model update\n'
        '4. Transparency: Communicate fairness metrics ke stakeholders\n'
        '5. Best practices: Share fairness approach sebagai benchmark'
    )
    
    pdf.add_page()
    pdf.section_title('4.3. Skenario 3: Bias Moderat (Medium Severity)')
    pdf.body_text(
        'Dataset: 500 applicants (280 Young, 220 Old)\n\n'
        'Metrics:\n'
        '- Young Approval Rate: 68.5%\n'
        '- Old Approval Rate: 52.3%\n'
        '- Approval Gap: 16.2%\n'
        '- Young Avg Score: 625\n'
        '- Old Avg Score: 585\n'
        '- Score Gap: 40 points\n'
        '- DI Ratio: 0.763\n'
        '- T-Test p-value: 0.012\n'
        '- Cohen\'s d: 0.42\n\n'
        'Interpretasi:\n'
        '1. Approval Gap 16.2% mendekati 20% threshold -> MODERAT, perlu monitoring\n'
        '2. Score Gap 40 points < 100 threshold -> Tidak major concern, tapi notable\n'
        '3. DI Ratio 0.763 < 0.80 -> FAIL 80% Rule (borderline)\n'
        '4. p-value 0.012 < 0.05 -> SIGNIFICANT\n'
        '5. Cohen\'s d 0.42 (0.2-0.5) -> SMALL to MEDIUM EFFECT\n\n'
        'Kesimpulan:\n'
        'MODERATE BIAS DETECTED. System menunjukkan perbedaan treatment yang signifikan secara statistik, '
        'meskipun magnitude-nya tidak sebesar high severity case. DI Ratio sedikit di bawah 80% threshold (76.3%), '
        'mengindikasikan potential adverse impact. Effect size (Cohen\'s d = 0.42) termasuk small-to-medium.\n\n'
        'Severity Level: MEDIUM (Investigation and intervention recommended)\n\n'
        'Rekomendasi:\n'
        '1. Investigation: Analyze model features, check for proxy discrimination\n'
        '2. Feature audit: Review fitur yang berkorelasi dengan Age (misal: Employment_Years)\n'
        '3. Threshold adjustment: Pertimbangkan adjust approval threshold untuk fairness\n'
        '4. Fairness constraints: Implement demographic parity atau equalized odds constraints\n'
        '5. Monitoring: Deploy real-time bias monitoring\n'
        '6. Periodic re-assessment: Re-audit tiap bulan untuk track improvement'
    )
    
    # Chapter 5: Visualizations Guide
    pdf.add_page()
    pdf.chapter_title('5. PANDUAN VISUALISASI')
    
    pdf.section_title('5.1. Distribution Analysis Charts')
    pdf.body_text(
        '1. Histogram (Overlapping):\n'
        '   - Menampilkan distribusi credit score untuk Young (Navy Blue) dan Old (Grey)\n'
        '   - Cara baca: Jika 2 histogram TERPISAH JAUH = bias kuat\n'
        '   - Jika OVERLAP banyak = distribusi mirip, fair\n\n'
        '2. Box Plot:\n'
        '   - Menampilkan quartile (Q1, median, Q3) dan outliers\n'
        '   - Cara baca: Bandingkan MEDIAN (garis tengah kotak)\n'
        '   - Jika median Young >> median Old = bias\n\n'
        '3. Violin Plot:\n'
        '   - Kombinasi box plot + kernel density plot\n'
        '   - Bagian LEBAR = banyak data di range tersebut\n'
        '   - Cara baca: Lihat shape dan overlap\n'
        '   - Jika shape TIDAK OVERLAP = bias kuat'
    )
    
    pdf.section_title('5.2. Income vs Score Charts')
    pdf.body_text(
        '1. Bubble Scatter Plot:\n'
        '   - X-axis: Annual Income, Y-axis: Credit Score\n'
        '   - Bubble size: Credit Score (makin besar = makin tinggi)\n'
        '   - Warna: Navy (Young), Grey (Old)\n'
        '   - Cara baca: Jika Grey SELALU DI BAWAH Navy = bias across ALL income levels\n\n'
        '2. Age-Score Trend Line:\n'
        '   - Line chart: Age (20-66) vs Average Score\n'
        '   - Shaded area: Confidence band (standard deviation)\n'
        '   - Vertical line: Age 45 (threshold)\n'
        '   - Cara baca: Jika garis TERJUN di age 45 = clear bias pattern'
    )
    
    pdf.section_title('5.3. Advanced Charts')
    pdf.body_text(
        '1. Correlation Heatmap:\n'
        '   - Matrix korelasi semua numerical features\n'
        '   - Warna: Navy (high correlation), Grey (low)\n'
        '   - Cara baca: Cari cell Age vs Credit Score\n'
        '   - Nilai negatif tinggi (misal -0.9) = strong negative correlation = bias\n'
        '   - Juga cari PROXY features (Employment_Years vs Age)\n\n'
        '2. Fairness Radar Chart:\n'
        '   - Pentagon dengan 5 fairness metrics\n'
        '   - Reference line di 80 (threshold)\n'
        '   - Cara baca: Jika blue line DI BAWAH threshold = FAIL metric tersebut\n\n'
        '3. Sunburst Chart:\n'
        '   - Hierarchical: Age Group -> Risk Category -> Loan Status\n'
        '   - Interactive: Klik untuk drill-down\n'
        '   - Cara baca: Bandingkan proporsi warna per age group'
    )
    
    # Chapter 6: References (Extended)
    pdf.add_page()
    pdf.chapter_title('6. REFERENSI DAN TINJAUAN PUSTAKA')
    
    pdf.section_title('6.1. Legal and Regulatory Framework')
    pdf.add_bullet('EEOC (1978). Uniform Guidelines on Employee Selection Procedures. Federal Register, Vol. 43, No. 166. '
                   'Established the 80% Rule (Four-Fifths Rule) for adverse impact analysis.')
    pdf.add_bullet('Age Discrimination in Employment Act (ADEA) of 1967. Protects individuals 40 years and older from age-based discrimination.')
    pdf.add_bullet('Equal Credit Opportunity Act (ECOA) of 1974. Prohibits discrimination in credit transactions based on protected attributes.')
    pdf.add_bullet('Undang-Undang No. 8 Tahun 1999 tentang Perlindungan Konsumen. Indonesia consumer protection law.')
    pdf.add_bullet('OJK Regulation No. 1/POJK.07/2013 on Consumer Protection in Financial Services Sector.')
    pdf.add_bullet('ISO/IEC 24027:2021. Information technology - Artificial intelligence - Bias in AI systems and AI aided decisions.')
    pdf.ln(3)
    
    pdf.section_title('6.2. Academic Literature on Algorithmic Fairness')
    pdf.add_bullet('Barocas, S., & Selbst, A. D. (2016). Big Data\'s Disparate Impact. California Law Review, 104, 671-732. '
                   'Seminal paper on how big data analytics can produce discriminatory outcomes.')
    pdf.add_bullet('Feldman, M., Friedler, S. A., Moeller, J., Scheidegger, C., & Venkatasubramanian, S. (2015). '
                   'Certifying and Removing Disparate Impact. ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.')
    pdf.add_bullet('Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). '
                   'A Survey on Bias and Fairness in Machine Learning. ACM Computing Surveys, 54(6), 1-35.')
    pdf.add_bullet('Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. '
                   'Big Data, 5(2), 153-163.')
    pdf.add_bullet('Hardt, M., Price, E., & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. '
                   'Advances in Neural Information Processing Systems (NeurIPS).')
    pdf.ln(3)
    
    pdf.add_page()
    pdf.section_title('6.3. Statistical Methods')
    pdf.add_bullet('Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.). Lawrence Erlbaum Associates. '
                   'Classic reference for effect size interpretation.')
    pdf.add_bullet('Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. '
                   'Annals of Mathematical Statistics, 18(1), 50-60.')
    pdf.add_bullet('Student (1908). The probable error of a mean. Biometrika, 6(1), 1-25. Original T-Test paper.')
    pdf.ln(3)
    
    pdf.section_title('6.4. Fairness Metrics and Frameworks')
    pdf.add_bullet('Verma, S., & Rubin, J. (2018). Fairness Definitions Explained. '
                   'ACM/IEEE International Workshop on Software Fairness. Comprehensive survey of 20+ fairness definitions.')
    pdf.add_bullet('Dwork, C., Hardt, M., Pitassi, T., Reingold, O., & Zemel, R. (2012). '
                   'Fairness Through Awareness. ACM Innovations in Theoretical Computer Science Conference.')
    pdf.ln(3)
    
    pdf.section_title('6.5. Tools and Software')
    pdf.add_bullet('McKinney, W. (2010). Data Structures for Statistical Computing in Python. '
                   'Proceedings of the 9th Python in Science Conference. Pandas library.')
    pdf.add_bullet('Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. '
                   'Nature Methods, 17, 261-272.')
    pdf.add_bullet('Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. '
                   'Journal of Machine Learning Research, 12, 2825-2830.')
    pdf.add_bullet('Plotly Technologies Inc. (2015). Collaborative Data Science. Montreal, QC: Plotly Technologies Inc.')
    pdf.ln(3)
    
    pdf.section_title('6.6. Industry Best Practices')
    pdf.add_bullet('Google AI. (2020). Responsible AI Practices. https://ai.google/responsibilities/responsible-ai-practices/')
    pdf.add_bullet('Microsoft. (2022). Responsible AI Standard v2. Microsoft AI principles and practices.')
    pdf.add_bullet('IBM. (2020). AI Fairness 360: An Extensible Toolkit for Detecting and Mitigating Algorithmic Bias. '
                   'IBM Journal of Research and Development.')
    
    # Final page
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 43, 91)
    pdf.cell(0, 10, 'END OF GUIDE', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, 'For technical support or questions:', 0, 1, 'C')
    pdf.cell(0, 6, 'Refer to CARA_PAKAI_LENGKAP.md, CHEAT_SHEET.md, or VISUAL_GUIDE.md', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, 'AI Bias Auditor v3.0 - Advanced Edition', 0, 1, 'C')
    pdf.cell(0, 5, 'Audit Teknologi dan Sistem Informasi 2025', 0, 1, 'C')
    pdf.cell(0, 5, f'Document generated: {datetime.now().strftime("%d %B %Y, %H:%M")}', 0, 1, 'C')
    
    return pdf


def save_pdf(pdf, filename):
    """Save PDF to file."""
    pdf.output(filename)
    return filename
