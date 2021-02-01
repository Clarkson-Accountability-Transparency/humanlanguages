#In English, Spanish, French, German all profession words occur in the corpus
df_english <- read_csv("../professionSetsByLanguage/english_results.csv")
#df2 <- read_csv("arabic_results2.csv")
df_spanish <- read_csv("../professionSetsByLanguage/spanish_even.csv")
df_german <- read_csv("../professionSetsByLanguage/german_even.csv")
df_french <- read_csv("../professionSetsByLanguage/french_even.csv")

#TODO-I'm not sure I am choosing the right Chinese results column
df_chinese <- read_csv("../professionSetsByLanguage/chinese_results_pca0.csv")
df_chinese_pca1 <- read_csv("../professionSetsByLanguage/chinese_results_pca1.csv")

#in Farsi journalist, astronomer and biologist do not occur in corpus
df_farsi <- read_csv("../professionSetsByLanguage/farsi_results.csv")

#in Arabic, filmmaker, astronaut and astronomer do not occur in the corpus
df_arabic <- read_csv("../professionSetsByLanguage/arabic_even.csv")

#in Urdu comedian, adventurer, analyst, astronomer and biologist do not occur in the corpus
#Also we have English words transcribed in Arabic character set for 9 words - could those be considered neutral words?
#Only 2 female profession variants occur in the corpus - teacher and actor
df_urdu <- read_csv("../professionSetsByLanguage/urdu_even.csv")

#In Wolof only two profession words - person and musician appear in the corpus
df_wolof <- read_csv("../professionSetsByLanguage/wolof_results.csv")


#For Gendered languages, read in female, male and neutral separately
df_spanish_female <-read_csv("../professionSetsByLanguage/spanish_female.csv")
df_spanish_male <-read_csv("../professionSetsByLanguage/spanish_male.csv")
df_spanish_neutral <-read_csv("../professionSetsByLanguage/spanish_neutral.csv")
df_spanish_weighted <-read_csv("../professionSetsByLanguage/spanish_weighted.csv")
df_spanish_weighted_simple <-read_csv("../professionSetsByLanguage/spanish_weighted.csv")

df_french_female <-read_csv("../professionSetsByLanguage/french_female.csv")
df_french_male <-read_csv("../professionSetsByLanguage/french_male.csv")
df_french_neutral <-read_csv("../professionSetsByLanguage/french_neutral.csv")
df_french_weighted <-read_csv("../professionSetsByLanguage/french_weighted.csv")
df_french_weighted_simple <-read_csv("../professionSetsByLanguage/french_weighted.csv")

df_german_female <-read_csv("../professionSetsByLanguage/german_female.csv")
df_german_male <-read_csv("../professionSetsByLanguage/german_male.csv")
df_german_neutral <-read_csv("../professionSetsByLanguage/german_neutral.csv")
df_german_weighted <-read_csv("../professionSetsByLanguage/german_weighted.csv")
df_german_weighted_simple <-read_csv("../professionSetsByLanguage/german_weighted.csv")

#Note Arabic character's lost in CSV
df_arabic_female <-read_csv("../professionSetsByLanguage/arabic_female.csv")
df_arabic_male <-read_csv("../professionSetsByLanguage/arabic_male.csv")
df_arabic_neutral <-read_csv("../professionSetsByLanguage/arabic_neutral.csv")
df_arabic_weighted <-read_csv("../professionSetsByLanguage/arabic_weighted.csv")
df_arabic_weighted_simple <-read_csv("../professionSetsByLanguage/arabic_weighted.csv")


df_urdu_female <-read_csv("../professionSetsByLanguage/urdu_female.csv")
df_urdu_male <-read_csv("../professionSetsByLanguage/urdu_male.csv")
df_urdu_neutral <-read_csv("../professionSetsByLanguage/urdu_neutral.csv")
df_urdu_english <-read_csv("../professionSetsByLanguage/urdu_english.csv")
df_urdu_weighted <-read_csv("../professionSetsByLanguage/urdu_weighted.csv")
df_urdu_weighted_simple <-read_csv("../professionSetsByLanguage/urdu_weighted.csv")



######################################################################################################

#Add language variable in each 
df_english <- df_english %>% 
  mutate(language = "English")

df_farsi <- df_farsi %>%
  mutate(language = "Farsi")

df_chinese <- df_chinese %>% 
  mutate(language = "Chinese")


df_chinese_pca0 <- df_chinese %>% 
  mutate(gender = "PCA0")
df_chinese_pca1 <- df_chinese_pca1 %>% 
  mutate(language = "Chinese")%>%
  mutate(gender = "PCA1")


df_wolof <- df_wolof %>%
  mutate(language = "Wolof")


df_arabic <- df_arabic %>% 
  mutate(language = "Arabic")
df_arabic_combo <- df_arabic %>%
  mutate(Arabic = "EMPTY") %>%
  mutate(gender = "Weighted Equally")
df_arabic_weighted_simple <- df_arabic_weighted_simple %>%
  mutate(language = "Arabic")
df_arabic_weighted <- df_arabic_weighted %>%
  mutate(language = "Arabic")%>%
  mutate(Arabic = "EMPTY") %>%
  mutate(gender = "Weighted By Word Count")
df_arabic_female <- df_arabic_female %>%
  mutate(language = "Arabic") %>%
  mutate(gender = "Female")
df_arabic_male <- df_arabic_male %>%
  mutate(language = "Arabic")%>%
  mutate(gender = "Male")
df_arabic_neutral <- df_arabic_neutral %>%
  mutate(language = "Arabic")%>%
  mutate(gender = "Neutral")



df_spanish <- df_spanish %>%
  mutate(language = "Spanish")
df_spanish_combo <- df_spanish %>%
  mutate(Spanish = "EMPTY") %>%
  mutate(gender = "Weighted Equally")
df_spanish_weighted_simple <- df_spanish_weighted_simple %>%
  mutate(language = "Spanish")
df_spanish_weighted <- df_spanish_weighted %>%
  mutate(language = "Spanish")%>%
  mutate(Spanish = "EMPTY") %>%
  mutate(gender = "Weighted By Word Count")
df_spanish_female <- df_spanish_female %>%
  mutate(language = "Spanish") %>%
  mutate(gender = "Female")
df_spanish_male <- df_spanish_male %>%
  mutate(language = "Spanish")%>%
  mutate(gender = "Male")
df_spanish_neutral <- df_spanish_neutral %>%
  mutate(language = "Spanish")%>%
  mutate(gender = "Neutral")


df_french <- df_french %>%
  mutate(language = "French")
df_french_combo <- df_french %>%
  mutate(French = "EMPTY") %>%
  mutate(gender = "Weighted Equally")
df_french_weighted_simple <- df_french_weighted_simple %>%
  mutate(language = "French")
df_french_weighted <- df_french_weighted %>%
  mutate(language = "French")%>%
  mutate(French = "EMPTY") %>%
  mutate(gender = "Weighted By Word Count")
df_french_female  <- df_french_female  %>%
  mutate(language = "French")%>%
  mutate(gender = "Female")
df_french_male  <- df_french_male %>%
  mutate(language = "French")%>%
  mutate(gender = "Male")
df_french_neutral <- df_french_neutral %>%
  mutate(language = "French")%>%
  mutate(gender = "Neutral")

df_german <- df_german %>%
  mutate(language = "German")
df_german_combo <- df_german %>%
  mutate(German = "EMPTY") %>%
  mutate(gender = "Weighted Equally")
df_german_weighted_simple <- df_german_weighted_simple %>%
  mutate(language = "German")
df_german_weighted <- df_german_weighted %>%
  mutate(language = "German")%>%
  mutate(German = "EMPTY") %>%
  mutate(gender = "Weighted By Word Count")
df_german_female <- df_german_female %>%
  mutate(language = "German")%>%
  mutate(gender = "Female")
df_german_male <- df_german_male %>%
  mutate(language = "German")%>%
  mutate(gender = "Male")
df_german_neutral <- df_german_neutral %>%
  mutate(language = "German")%>%
  mutate(gender = "Neutral")


df_urdu <- df_urdu %>% 
  mutate(language = "Urdu")
df_urdu_combo <- df_urdu %>%
  mutate(Urdu = "EMPTY") %>%
  mutate(gender = "Weighted Equally")
df_urdu_weighted_simple <- df_urdu_weighted_simple %>%
  mutate(language = "Urdu")
df_urdu_weighted <- df_urdu_weighted %>%
  mutate(language = "Urdu")%>%
  mutate(Urdu = "EMPTY") %>%
  mutate(gender = "Weighted By Word Count")
df_urdu_female <- df_urdu_female %>%
  mutate(language = "Urdu")%>%
  mutate(gender = "Female")
df_urdu_male <- df_urdu_male %>%
  mutate(language = "Urdu") %>%
  mutate(gender = "Male")
df_urdu_neutral <- df_urdu_neutral %>%
  mutate(language = "Urdu")%>%
  mutate(gender = "Urdu Neutral")
df_urdu_english <- df_urdu_english %>%
  mutate(language = "Urdu")%>%
  mutate(gender = "English Neutral")


######################################################################################

df_total <-  rbind(df_english, df_chinese, df_arabic, df_spanish, df_german, df_farsi, df_french, df_urdu, df_wolof)

df_total_weighted <-  rbind(df_english, df_chinese, df_arabic_weighted_simple, df_farsi, df_french_weighted_simple, df_urdu_weighted_simple, df_wolof, df_spanish_weighted_simple, df_german_weighted_simple)

df_gendered_languages <-rbind(df_spanish, df_german, df_arabic, df_french, df_urdu)

df_gendered_languages_weighted <-rbind(df_spanish_weighted_simple, df_german_weighted_simple, df_french_weighted_simple, df_arabic_weighted_simple, df_urdu_weighted_simple)

df_nongendered_languages<-rbind(df_english, df_chinese, df_farsi, df_wolof)

df_spanish_all <-rbind(df_spanish_female, df_spanish_male, df_spanish_neutral, 
                       df_spanish_combo, df_spanish_weighted)
df_french_all <-rbind(df_french_female, df_french_male, df_french_neutral, 
                      df_french_combo, df_french_weighted)
df_german_all <-rbind(df_german_female, df_german_male, df_german_neutral,
                      df_german_combo, df_german_weighted)

df_arabic_all <-rbind(df_arabic_female, df_arabic_male, df_arabic_neutral,
                      df_arabic_combo, df_arabic_weighted)
df_urdu_all <-rbind(df_urdu_female, df_urdu_male, df_urdu_neutral, df_urdu_english, df_urdu_combo, df_urdu_weighted)

df_chinese_all <-rbind(df_chinese_pca0, df_chinese_pca1)

####################################################################################################



#All languages weighted evenly 
df_maply <- df_total %>% 
  select(-pos) %>%
  spread(language, gender_bias)

df_maply <- as.data.frame(df_maply)

row.names(df_maply) <- df_maply$professions

df_maply <- df_maply %>% select(-professions)

heatmaply(
  df_maply, 
  scale_fill_gradient_fun = ggplot2::scale_fill_gradientn(
    colors = c("blue","white","red"),
    values=rescale(c(-0.4,0,0.4)),
    limits=c(-0.4,0.4)
  )
)

## All languages weighted evenly, no chinese or Wolof

df_total2 <-  rbind(df_english, df_arabic, df_spanish, df_german, df_farsi, df_french, df_urdu)

df_maply <- df_total2 %>% 
  select(-pos) %>%
  spread(language, gender_bias)

df_maply <- as.data.frame(df_maply)

row.names(df_maply) <- df_maply$professions

df_maply <- df_maply %>% select(-professions)

heatmaply(
  df_maply, 
  xlab = "Language",
  main = "Profession Set (Weighted Evenly)",
  scale_fill_gradient_fun = ggplot2::scale_fill_gradientn(
    colors = c("blue","white","red"),
    values=rescale(c(-0.4,0,0.4)),
    limits=c(-0.4,0.4)
  )
)


########################################################################################################

## Just English & Farsi, Look at Professions Clustering
df_eng_fars <- rbind(df_english, df_farsi)
df_maply <- df_eng_fars %>% 
  select(-pos) %>%
  spread(language, gender_bias)

df_maply <- as.data.frame(df_maply)

row.names(df_maply) <- df_maply$professions

df_maply <- df_maply %>% select(-professions)

heatmaply(
  df_maply, 
  scale_fill_gradient_fun = ggplot2::scale_fill_gradientn(
    colors = c("blue","white","red"),
    values=rescale(c(-0.4,0,0.4)),
    limits=c(-0.4,0.4),
    row
  )
)

#########################################################################################

## Weighted average 

df_maply <- df_total_weighted %>% 
  select(-pos) %>%
  spread(language, gender_bias)

df_maply <- as.data.frame(df_maply)

row.names(df_maply) <- df_maply$professions

df_maply <- df_maply %>% select(-professions)

heatmaply(
  df_maply, 
  scale_fill_gradient_fun = ggplot2::scale_fill_gradientn(
    colors = c("blue","white","red"),
    values=rescale(c(-0.4,0,0.4)),
    limits=c(-0.4,0.4),
    row
  )
)

######################################################################################################

## Taking Out Wolof and Chinese

df_total_weighted2 <-  rbind(df_english, df_arabic_weighted_simple, df_farsi,
                             df_french_weighted_simple, df_urdu_weighted_simple, 
                             df_spanish_weighted_simple, df_german_weighted_simple)

df_maply <- df_total_weighted2 %>% 
  select(-pos) %>%
  spread(language, gender_bias)

df_maply <- as.data.frame(df_maply)

row.names(df_maply) <- df_maply$professions

df_maply <- df_maply %>% select(-professions)

heatmaply(
  df_maply, 
  xlab = "Language",
  main = "Profession Set (Weighted Average)",
  scale_fill_gradient_fun = ggplot2::scale_fill_gradientn(
    colors = c("blue","white","red"),
    values=rescale(c(-0.4,0,0.4)),
    limits=c(-0.4,0.4)
  )
)



