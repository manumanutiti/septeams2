from functions import SepTeam

sep = SepTeam()

### Pseudo ###

pseudo_names = ["Zorix", "Lumen", "Taris", "Sivel", "Nydra", "Voren", "Kaira", "Elvin", "Zaris",\
                "Relon", "Tirin", "Almen", "Oulen", "Bayl", "Nist", "Cloud", "El"]


### INFO ###
info_global = f"Este gráfico muestra los datos del equipo basado en la media global de todas las valoraciones,\
        por lo tanto no es la muestra visual más representativa, pero da idea una general sobre la constancia en el tiempo\
        y es un punto de apoyo para guiarnos con otros graficos"
        

info_last_survey = "Este gráfico muestra las valoraciones de la última encuesta. Las lineas rojas representan\
        las medias en los dos aspectos auditables (trabajo en equipo y Hard Skills)\
        El área verde (esquina derecha) agrupa a las personas que superan ambas medias.\
        El área amarilla recoge a personas con buenas habilidades técnicas pero peores \
        habilidades comunicativas y de equipo. El área roja es la 'zona de mejora', las personas en este\
        rectángulo ya pueden ser nuevos empleados, compañeros desmotivados o quizás reflejar un problema \
        del que no se tiene constancia y que puede ser evitado antes de que explote."

info_team_work_evolution = "Evolución de las valoraciones sobre el trabajo en equipo a lo largo del tiempo"

info_hard_skill_evolution = "Evolución de las valoraciones sobre las habilidades técnicas a lo largo del tiempo"



#### STATS #####

# ALL TIME MEANS
tw_and_hs_global_mean = sep.global_mean()
all_time_stats = (
        f"Team Work All Time Mean: {tw_and_hs_global_mean[0]}<br>"
        f"Hard Skills All Time Mean: {tw_and_hs_global_mean[1]}"
    )

# LAST SURVEY MEAN
tw_and_hs_last_mean = sep.last_mean()
last_survey_stats = (f"Team Work Last Survey Mean: {tw_and_hs_last_mean[0]}<br>"
                     f"Hard Skills Last Survey Mean: {tw_and_hs_last_mean[1]}"
)


if __name__ == '__main__':
        print(tw_and_hs_last_mean)