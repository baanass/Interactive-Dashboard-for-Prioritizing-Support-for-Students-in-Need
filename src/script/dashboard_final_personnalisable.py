import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'application
st.title('Élèves en difficulté à prioriser ')

# Interface pour télécharger le fichier CSV
uploaded_file = st.file_uploader("Téléchargez un fichier CSV", type=['csv'])

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

    # Affichage des premières lignes du DataFrame pour vérification
    st.write("Aperçu des premières lignes du fichier téléchargé :")
    st.write(df.head())

    # Liste des colonnes attendues dans le fichier CSV
    colonnes_attendues = ['StudentID', 'FamilyName', 'FirstName', 'sex', 'age', 'address', 'famsize', 'Pstatus', 
                          'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian', 
                          'traveltime', 'studytime', 'failures', 'schoolsup', 
                          'famsup', 'paid', 'activities', 'nursery', 'higher', 
                          'internet', 'romantic', 'famrel', 'freetime', 'goout', 
                          'Dalc', 'Walc', 'health', 'absences', 'FinalGrade']

    # Vérification de la présence des colonnes attendues
    colonnes_manquantes = [colonne for colonne in colonnes_attendues if colonne not in df.columns]

    if len(colonnes_manquantes) == 0:
        st.success("Toutes les colonnes requises sont présentes dans le fichier CSV.")

        # Interface pour définir les poids des paramètres
        st.sidebar.subheader('Définir les poids des paramètres')
        poids_failures = st.sidebar.slider('Poids pour la réussite', min_value=0.0, max_value=1.0, value=0.3, step=0.05)
        poids_goout = st.sidebar.slider('Poids pour la sociabilisation positive', min_value=0.0, max_value=1.0, value=0.19, step=0.05)
        poids_dalc = st.sidebar.slider('Poids pour  la sobriété durant la semaine', min_value=0.0, max_value=1.0, value=0.15, step=0.05)
        poids_walc = st.sidebar.slider('Poids pour  la sobriété durant le weekend', min_value=0.0, max_value=1.0, value=0.19, step=0.05)
        poids_absences = st.sidebar.slider('Poids pour assiduité', min_value=0.0, max_value=1.0, value=0.24, step=0.05)
        poids_studytime = st.sidebar.slider('Poids pour temps d\'étude', min_value=0.0, max_value=1.0, value=0.11, step=0.05)


        # Exemple de normalisation pour certains paramètres
        df['failures'] = (df['failures'] - df['failures'].mean()) / df['failures'].std()
        df['goout'] = (df['goout'] - df['goout'].mean()) / df['goout'].std()
        df['Dalc'] = (df['Dalc'] - df['Dalc'].mean()) / df['Dalc'].std()
        df['Walc'] = (df['Walc'] - df['Walc'].mean()) / df['Walc'].std()
        df['absences'] = (df['absences'] - df['absences'].mean()) / df['absences'].std()
        df['studytime'] = (df['studytime'] - df['studytime'].mean()) / df['studytime'].std()

        # Inverser les paramètres péjoratifs en les soustrayant de la valeur maximale
        df['inverse_failures'] = df['failures'].max() - df['failures']
        df['inverse_goout'] = df['goout'].max() - df['goout']
        df['inverse_Dalc'] = df['Dalc'].max() - df['Dalc']
        df['inverse_Walc'] = df['Walc'].max() - df['Walc']
        df['inverse_absences'] = df['absences'].max() - df['absences']

        # Calcul de l'Improvement Score avec les poids définis par l'utilisateur
        df['Improvement Score'] = (poids_failures * df['inverse_failures'] +
                                   poids_goout * df['inverse_goout'] +
                                   poids_dalc * df['inverse_Dalc'] +
                                   poids_walc * df['inverse_Walc'] +
                                   poids_absences * df['inverse_absences'] +
                                   poids_studytime * df['studytime'])

        # Définir le seuil pour la note finale en mathématiques
        seuil_note = 10

        # Filtrage des étudiants avec une note finale basse mais un bon Improvement Score
        students_to_highlight = df[(df['FinalGrade'] < seuil_note) ]

        # Création du Scatter Plot interactif avec Plotly Express pour tous les élèves
        fig_all_students = px.scatter(df, x='FinalGrade', y='Improvement Score', color='age',
                                      labels={'FinalGrade': 'Note finale en mathématiques', 'Improvement Score': 'Improvement Score'})

        # Personnalisation du layout du graphique pour tous les élèves
        fig_all_students.update_layout(title='Tous les élèves',
                                       xaxis_title='Note finale en mathématiques',
                                       yaxis_title='Improvement Score')
        # Mise à jour des traces pour rendre les points cliquables
        fig_all_students.update_traces(mode='markers', marker={'size': 10},
                                               customdata=df[['StudentID', 'FamilyName', 'FirstName']].values,
                                               hovertemplate='<b>Student ID:</b> %{customdata[0]}<br>'
                                                             '<b>FamilyName:</b> %{customdata[1]}<br>'
                                                             '<b>FirstName:</b> %{customdata[2]}<br>')

        # Création du Scatter Plot interactif avec Plotly Express pour les élèves à mettre en évidence
        fig_highlighted_students = px.scatter(students_to_highlight, x='FinalGrade', y='Improvement Score', color='age',
                                              labels={'FinalGrade': 'Note finale en mathématiques', 'Improvement Score': 'Improvement Score'})

        # Personnalisation du layout du graphique pour les élèves à mettre en évidence
        fig_highlighted_students.update_layout(title='Zoom sur les élèves avec une note en mathématiques en dessous de la moyenne',
                                               xaxis_title='Note finale en mathématiques',
                                               yaxis_title='Improvement Score')

        # Mise à jour des traces pour rendre les points cliquables
        fig_highlighted_students.update_traces(mode='markers', marker={'size': 10},
                                               customdata=students_to_highlight[['StudentID', 'FamilyName', 'FirstName']].values,
                                               hovertemplate='<b>Student ID:</b> %{customdata[0]}<br>'
                                                             '<b>FamilyName:</b> %{customdata[1]}<br>'
                                                             '<b>FirstName:</b> %{customdata[2]}<br>')

        # Affichage du Scatter Plot interactif pour tous les élèves
        st.plotly_chart(fig_all_students)

        # Affichage du Scatter Plot interactif pour les élèves à mettre en évidence
        st.plotly_chart(fig_highlighted_students)

        # Affichage du classement des élèves à prendre en charge
        st.subheader('Les élèves en difficultés à prendre en charge :')
        # Trier les étudiants à mettre en évidence d'abord par FinalGrade, puis par Improvement Score
        students_sorted = students_to_highlight.sort_values(by=['FinalGrade', 'Improvement Score'], ascending=[True, False])
        # Affichage du classement des élèves à prendre en charge
        st.write(students_sorted[['StudentID', 'FamilyName', 'FirstName', 'Improvement Score', 'FinalGrade']])

        
    else:
        st.error(f"Les colonnes suivantes sont manquantes : {', '.join(colonnes_manquantes)}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer l'analyse.")
