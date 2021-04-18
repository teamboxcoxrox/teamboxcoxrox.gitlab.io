df_rank <-  read.csv('ranking.csv')
df_sent <-  read.csv('pets_sentiment_grouped.csv')

df_rank$mean_rank <-  df_rank$overall_average
df_sent$mean_sentiment <-  df_sent$mean

df <-  merge(x = df_rank, y = df_sent, by = "asin", all.x = TRUE)
df_filt <-  df[df$overall_count >= 10,]

mdl = lm(mean_rank~mean_sentiment, data=df_filt)
plot(df_filt$mean_sentiment, df_filt$mean_rank)
summary(mdl)
