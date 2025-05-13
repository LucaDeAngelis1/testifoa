import joblib
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io

def convert_to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="data",index=False)
    # see: https://xlsxwriter.readthedocs.io/working_with_pandas.html
    writer.close()
    return output.getvalue()

def fig2(df1):
    fig2, axes2 = plt.subplots(2, 2, figsize=(15,8))
    sns.violinplot(x='class', y='sepal length', data=df1, hue="class", ax=axes2[0,0])
    sns.violinplot(x='class', y='sepal width', data=df1, hue="class", ax=axes2[0,1])
    sns.violinplot(x='class', y='petal length', data=df1, hue="class", ax=axes2[1,0])
    sns.violinplot(x='class', y='petal width', data=df1, hue="class", ax=axes2[1,1])
    plt.tight_layout()
    return fig2

def main():
    st.title("Analisi Dati")
    url = st.text_input('Incolla dataset url:',"https://frenzy86.s3.eu-west-2.amazonaws.com/fav/iris.data")
    df = pd.read_csv(url, header=None)
    df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
    df1 = df.copy()
    st.dataframe(df1)

    tab1, tab2, tab3, tab4, = st.tabs(["tab1", "tab2", "tab3", "tab4"])

    with tab1:
        if st.button('Statistiche', help="Process Dataframe"):
            st.subheader('📈 Statistiche Descrittive')
            st.dataframe(df1.describe())

    with tab2:
        if st.button('Grafici', help="Process Dataframe"):
            st.subheader('🎨 Pairplot delle Variabili Selezionate')
            fig = sns.pairplot(df1, hue='class', diag_kind='kde',height=4)
            st.pyplot(fig)

            st.subheader('🎨 Violinplot delle Variabili Selezionate')
            st.pyplot(fig2(df1))

            st.subheader('🎨 Countplot delle Variabili Selezionate')
            fig3, axes = plt.subplots()
            sns.countplot(data=df1, x='sepal width', hue='class', ax=axes)
            st.pyplot(fig3)

            st.subheader('🎨 Jointplot delle Variabili Selezionate')
            fig4 = sns.jointplot(x='petal length', y='petal width', hue='class', data=df1, height=6)
            st.pyplot(fig4)

    with tab3:
        st.subheader(":magic_wand: Inferenza")

        sepal_length = st.slider('sepal length', 0.0, 6.5, 2.5)
        sepal_width = st.slider('sepal width', 0.0, 6.5, 2.5)
        petal_length = st.slider('petal length', 0.0, 6.5, 0.5)
        petal_width = st.slider('petal width', 0.0, 6.5, 0.5)

        data = {
            'sepal_length': [sepal_length],
            'sepal_width': [sepal_width],
            'petal_length': [petal_length],
            'petal_width': [petal_width]
        }

        pred_data = pd.DataFrame(data)

        iris_pipe = joblib.load('iris_pipe.pkl')

        if st.button('Prediction'):
            pred = iris_pipe.predict(pred_data)[0]
            # classes = {0: 'SETOSA',
            #            1: 'VERSICOLOR',
            #            2: 'VIRGINICA'}
            # y_pred = classes[pred]
            y_pred = pred
            st.success(y_pred)
    
    with tab4:
        st.title("Caricamento File CSV/XLSX")
        uploaded_file = st.file_uploader("Scegli un file CSV o XLSX", type=['csv', 'xlsx'])
        success_check = 0

        if uploaded_file is not None:
            # Verifica l'estensione del file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.success("File CSV caricato con successo!")
                success_check = 1
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                st.success("File XLSX caricato con successo!")
                success_check = 1
            else:
                st.error("Formato file non supportato!")

            st.dataframe(df)

            if success_check == 1:
                st.write("ok")
                if st.button('Start Processing', help="Process Dataframe"):
                    st.header('Adds Prediction')
                    df['predicted_class'] = iris_pipe.predict(df)
                    st.dataframe(df)
                    st.balloons()
                    st.download_button(
                                        label="download as Excel-file",
                                        data=convert_to_excel(df),
                                        file_name="data.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        key="excel_download",
                                        )

if __name__ == "__main__":
    main()