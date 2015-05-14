library(mallet)
files <- mallet.read.dir("/srv/data/multimodal/finnishsubset/")
texts <- files$text

# read in some stopwords:
library(tm)
stop_words <- stopwords("SMART")

# tokenize on space and output as a list:
mtexts <- texts
mtexts <- gsub("[0-9]+", "NUMBER", mtexts)  # replace punctuation with space
mtexts <- gsub("[[:punct:]]", " ", mtexts)  # replace punctuation with space
mtexts <- gsub("[[:cntrl:]]", " ", mtexts)  # replace control characters with space
mtexts <- gsub("^[[:space:]]+", "", mtexts) # remove whitespace at beginning of documents
mtexts <- gsub("[[:space:]]+$", "", mtexts) # remove whitespace at end of documents
mtexts <- tolower(mtexts)  # force to lowercase
doc.list <- strsplit(mtexts, "[[:space:]]+")

# compute the table of terms:
term.table <- table(unlist(doc.list))
term.table <- sort(term.table, decreasing = TRUE)

# remove terms that are stop words or occur fewer than 5 times:
del <- names(term.table) %in% stop_words | term.table < 5
term.table <- term.table[!del]
vocab <- names(term.table)

# now put the documents into the format required by the lda package:
get.terms <- function(x) {
  index <- match(x, vocab)
  index <- index[!is.na(index)]
  rbind(as.integer(index - 1), as.integer(rep(1, length(index))))
}
documents <- lapply(doc.list, get.terms)
# Compute some statistics related to the data set:
D <- length(documents)  # number of documents (2,000)
W <- length(vocab)  # number of terms in the vocab (14,568)
doc.length <- sapply(documents, function(x) sum(x[2, ]))  # number of tokens per document [312, 288, 170, 436, 291, ...]
N <- sum(doc.length)  # total number of tokens in the data (546,827)
term.frequency <- as.integer(term.table)  # frequencies of terms in the corpus [8939, 5544, 2411, 2410, 2143, ...]

# MCMC and model tuning parameters:
K <- 20
G <- 5000
alpha <- 0.02
eta <- 0.02

# Fit the model:
library(lda)
set.seed(357)
t1 <- Sys.time()
fit <- lda.collapsed.gibbs.sampler(documents = documents, K = K, vocab = vocab, 
                                   num.iterations = G, alpha = alpha, 
                                   eta = eta, initial = NULL, burnin = 0,
                                   compute.log.likelihood = TRUE)
t2 <- Sys.time()
t2 - t1  # about 24 minutes on laptop

theta <- t(apply(fit$document_sums + alpha, 2, function(x) x/sum(x)))
phi <- t(apply(t(fit$topics) + eta, 2, function(x) x/sum(x)))

textsLDA <- list(phi = phi,
                     theta = theta,
                     doc.length = doc.length,
                     vocab = vocab,
                     term.frequency = term.frequency)

library(LDAvis)

# create the JSON object to feed the visualization:
json <- createJSON(phi = textsLDA$phi, 
                   theta = textsLDA$theta, 
                   doc.length = textsLDA$doc.length, 
                   vocab = textsLDA$vocab, 
                   term.frequency = textsLDA$term.frequency)

serVis(json,out.dir="mmvis")

