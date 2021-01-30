library(tidyverse)
library(ggplot2)
library(ggrepel)

professions <- c("nurse", "teacher","writer","engineer", "scientist", "manager","driver", "banker", "musician", "artist", "chef", "filmmaker","judge",
                 "comedian", "inventor", "worker", "soldier", "journalist", "student", "athlete", "actor", "governor", "farmer", "person", "lawyer", 
                 "adventurer", "aide", "ambassador","analyst", "astronaut", "astronomer","biologist")
defining_set <- c("woman", "man", "daughter", "son", "mother", "father", "girl", "boy", "queen",
                  "king", "wife", "husband", "madam", "sir")

male <- c(FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE )

PCA_0_Professions <- c(
  0.05528912844,
  0.1523658308,
  0.02067633042,
  0.05529331082,
  0.1273388406,
  -0.05736198447,
  0.06471906746,
  0.1197431538,
  0.1173434641,
  0.1493684765,
  0.03777392656,
  0.2610610823,
  0.1020473033,
  0.07467208532,
  0.193105641,
  0.03033220483,
  0.1309692781,
  0.04408764908,
  0.1627991687,
  0.01112203698,
  0.2538277456,
  0.1907374712
)

PCA_1_Professions <- c(
  -0.293937017,
  -0.1330812678,
  -0.04671568244,
  -0.2058383421,
  -0.2742408337,
  -0.1973468572,
  -0.2374410216,
  -0.1788131862,
  -0.2620061859,
  -0.2380629497,
  -0.2294814503,
  -0.2262132406,
  -0.331283839,
  -0.03901860487,
  -0.2228431401,
  -0.3187676672,
  0.03031387333,
  -0.05339799636,
  -0.1667537601,
  -0.2235695043,
  -0.2011092588,
  -0.03720452575
)

PCA_0_def_CH <- c(
  -0.1775168445,
  -0.1987665366,
  0.2457352014,
  0.4251781014,
  0.2510986867,
  0.4114486879,
  -0.2697166835,
  -0.1698664731,
  -0.3057220659,
  0.3280819983,
  0.1898208639,
  0.1132699196,
  0.1079769493,
  -0.519040602
)

PCA_1_def_CH <- c(
  -0.1071820081,
  -0.145785364,
  -0.1047450205,
  -0.2268722679,
  -0.09025756756,
  -0.1086855443,
  -0.07554149737,
  -0.08096232675,
  0.1130676467,
  -0.4281297325,
  0.115581118,
  0.1047669621,
  0.2518643431,
  -0.3800878729
)

PCA_0_def_EN <- c(
  0.3924927844,
  -0.04411962919,
  0.04952435072,
  -0.2618651499,
  0.224662506,
  -0.1242408018,
  0.3712831473,
  -0.002329233498,
  0.1916616422,
  -0.2228449412,
  0.1164351189,
  0.05503665652,
  0.437653361,
  -0.5440336289
)

PCA_1_def_EN <- c(
  0.1090313256,
  -0.2506025834,
  0.3467324379,
  0.02096122029,
  0.203947749,
  -0.01672562375,
  0.007672721334,
  -0.1795319292,
  0.3786182371,
  -0.03719771606,
  0.2907017471,
  0.1678138361,
  -0.03833089531,
  0.4321018856
)

#Chinese
df1 <- tibble(
  words = defining_set,
  PCA_0 = PCA_0_def_CH,
  PCA_1 = PCA_1_def_CH,
  gender_male = male,
  language = rep("Chinese", length.out = 14)
)

#English
df2 <- tibble(
  words = defining_set,
  PCA_0 = PCA_0_def_EN,
  PCA_1 = PCA_1_def_EN,
  gender_male = male,
  language = rep("English", length.out = 14)
)

#Combine data frames
df <- bind_rows(df1, df2)

p <- ggplot(df) +
      geom_point(aes(x = PCA_0, y = PCA_1, colour =gender_male)) + 
      geom_vline(xintercept = 0, colour = "gray") +
      geom_hline(yintercept = 0, colour = "gray") +
      geom_text_repel(aes(PCA_0, PCA_1, label = words)) +
      facet_wrap(~language) + 
      theme_bw() +
      labs(
        x = "Dominant Component",
        y = "Second Most Dominant Component"
      ) + 
      theme(
        legend.position = "none",
        plot.title = element_text(size = 12)
      )

ggsave("figure3.png",p, width = 6, height = 2.5)
