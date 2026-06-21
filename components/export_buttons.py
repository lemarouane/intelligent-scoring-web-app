

# comment : import des bibliothèques streamlit et des services d'export 
import streamlit as st
# comment : import des services d'export pdf 
from services.pdf_export   import generate_pdf
# comment : import des services d'export word 
from services.word_export  import generate_word
# comment : import des services d'export excel 
from services.excel_export import generate_excel
# comment : import de la bibliothèque datetime 
from datetime import datetime

# comment : fonction qui permet de rendre les boutons d'export
def render_export_buttons(
    categorie: str,
    final_score: float,
    risk_class: str,
    decision: str,
    prob_default: str,
    rows: list,
    ia_analysis: str = "",
):
    st.markdown("### 📥 Exports du rapport")
    col1, col2, col3 = st.columns(3)
    ts = datetime.now().strftime("%Y%m%d_%H%M")


# comment : bouton pour télécharger le rapport en PDF
    with col1:
        pdf_bytes = generate_pdf(
            categorie, final_score, risk_class,
            decision, prob_default, rows, ia_analysis,
        )
        st.download_button(
            label="📄 Télécharger PDF",
            data=pdf_bytes,
            file_name=f"BOA_Scoring_{ts}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# comment : bouton pour télécharger le rapport en Word
    with col2:
        word_bytes = generate_word(
            categorie, final_score, risk_class,
            decision, prob_default, rows, ia_analysis,
        )
        st.download_button(
            label="📝 Télécharger Word",
            data=word_bytes,
            file_name=f"BOA_Scoring_{ts}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

# comment : bouton pour télécharger le rapport en Excel
    with col3:
        excel_bytes = generate_excel(
            categorie, final_score, risk_class,
            decision, prob_default, rows, ia_analysis,
        )
        st.download_button(
            label="📊 Télécharger Excel",
            data=excel_bytes,
            file_name=f"BOA_Scoring_{ts}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )