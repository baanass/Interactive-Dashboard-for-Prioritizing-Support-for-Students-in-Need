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
        
        # Vérification des types de données et des valeurs manquantes pour les colonnes importantes
        colonnes_importantes = ['studytime', 'failures', 'absences', 'FinalGrade']
        erreurs = []

        for colonne in colonnes_importantes:
            if df[colonne].isnull().any():
                erreurs.append(f"La colonne {colonne} contient des valeurs manquantes.")
            if not pd.api.types.is_numeric_dtype(df[colonne]):
                erreurs.append(f"La colonne {colonne} doit être de type numérique.")

        if len(erreurs) == 0:
            st.success("Toutes les colonnes importantes sont valides et ne contiennent pas de valeurs manquantes.")

            # Calcul de l'Improvement Score
            df['Improvement Score'] = (df['studytime'] * (5 - df['failures'])) / (1 + df['absences'])

            # Définir le seuil pour la note finale en mathématiques
            seuil_note = 10

            # Filtrage des étudiants avec une note finale basse mais un bon Improvement Score
            students_to_highlight = df[(df['FinalGrade'] < seuil_note) & (df['Improvement Score'] > 0.5)]

            # Création du Scatter Plot interactif avec Plotly Express pour tous les élèves
            fig_all_students = px.scatter(df, x='FinalGrade', y='Improvement Score', color='sex',
                                          hover_data=['age', 'studytime', 'failures', 'absences'],
                                          labels={'FinalGrade': 'Note finale en mathématiques', 'Improvement Score': 'Improvement Score'})

            # Personnalisation du layout du graphique pour tous les élèves
            fig_all_students.update_layout(title='Tous les élèves',
                                           xaxis_title='Note finale en mathématiques',
                                           yaxis_title='Improvement Score')

            # Création du Scatter Plot interactif avec Plotly Express pour les élèves à mettre en évidence
            fig_highlighted_students = px.scatter(students_to_highlight, x='FinalGrade', y='Improvement Score', color='sex',
                                                  hover_data=['age', 'studytime', 'failures', 'absences'],
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

            #Sous titre
            st.subheader('Analyse de l\'établissement')
            # Ajout d'une image PNG
            st.image('../../ressources/Formula.png', use_column_width=True)
            
            # Affichage du Scatter Plot interactif pour tous les élèves
            st.plotly_chart(fig_all_students)

            # Affichage du Scatter Plot interactif pour les élèves à mettre en évidence
            st.plotly_chart(fig_highlighted_students)

            # Affichage du classement des élèves à prendre en charge
            st.subheader('Les élèves en difficultés à prendre en charge :')
            st.write(students_to_highlight[['StudentID', 'FamilyName', 'FirstName', 'Improvement Score', 'FinalGrade']].sort_values(by='Improvement Score', ascending=False))
        
        else:
            for erreur in erreurs:
                st.error(erreur)
    
    else:
        st.error(f"Les colonnes suivantes sont manquantes : {', '.join(colonnes_manquantes)}")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer l'analyse.")
