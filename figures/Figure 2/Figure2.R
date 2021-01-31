## Figure 2 

library(readr)

pca_df <- read_csv("~/Documents/GitHub/humanlanguages/figures/Figure 2/PCA_results.csv")
names(pca_df) <- c("Language", "PCA [0]", "PCA [1]", "Diff")



p <- ggplot(pca_df, aes(x = reorder(Language, Diff), y = Diff)) + 
  geom_bar(stat = "identity", fill = "DarkGray") +
  coord_flip() +
  labs(
    title = "Difference in PCA Scores",
    subtitle = "PCA [0] - PCA [1]",
    x = "",
    y = "Difference"
  ) +
  geom_text(aes(label=round(Diff, digits = 2)), hjust=-.5, color="black", size=3.5, fontface = "bold") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 16),
        plot.subtitle = element_text(hjust = 0.5),
        text = element_text(family = "Gill Sans"),
        axis.text = element_text(size = 14),
        axis.title = element_text(size= 14)) 

ggsave("figure2.png", p, height = 3, width = 5)
