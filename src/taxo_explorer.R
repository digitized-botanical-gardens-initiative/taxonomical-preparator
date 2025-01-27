


usePackage <- function(p) {
  if (!is.element(p, installed.packages()[, 1])) {
    install.packages(p, dep = TRUE)
  }
  require(p, character.only = TRUE)
}

# This one below is to the the default CRAN repo

r <- getOption("repos")
r["CRAN"] <- "http://cran.us.r-project.org"
options(repos = r)
rm(r)
 
 

usePackage("rotl")
usePackage("readr")
usePackage("dplyr")
usePackage("igraph")
usePackage("plyr")
usePackage("gridExtra")
usePackage("ggfortify")
usePackage("ggtree")
usePackage("plotly")
usePackage("archive")
usePackage("collapsibleTree")


download.file('http://files.opentreeoflife.org/ott/ott3.3/ott3.3.tgz', destfile = "data/inputs/ott3.3.tgz", method = "wget", extra = "-r -p --random-wait")

# and opened from the tar archive

taxonomy <- read_delim(archive_read("data/inputs/ott3.3.tgz", file = "ott3.3/taxonomy.tsv"), col_types = cols(), delim = "|", escape_double = FALSE, trim_ws = TRUE )





taxa <- read.csv("./data/out/wd_inat_output.csv",sep=",")
taxa_list <- unique(taxa$species_name.value)

resolved_names <- tnrs_match_names(taxa_list)
resolved_names_filter <- resolved_names[-grep("incertae_sedis",resolved_names$flags),]
resolved_names_filter <- resolved_names_filter[!is.na(resolved_names_filter$flags),]
lineage_garden <-tax_lineage(taxonomy_taxon_info(resolved_names_filter$ott_id, include_lineage = TRUE))
lineage_garden_matt <- ldply(lineage_garden,rbind)

my_tree <- tol_induced_subtree(ott_ids = resolved_names_filter$ott_id)

lineage_garden_matt_wide <- reshape(lineage_garden_matt,
                                        idvar= ".id",
                                        timevar = "rank",
                                        direction="wide"
                                        )


 


lineage_garden_matt_short <- lineage_garden_matt_wide %>% 
                             select(".id","name.genus","name.family","name.order","name.class","name.domain")


resolved_names_filter$ott_id <- as.integer(resolved_names_filter$ott_id)
lineage_garden_matt_short$.id <- as.integer(lineage_garden_matt_short$.id)


taxonomy_clean <-
  left_join(resolved_names_filter,lineage_garden_matt_short,by=c("ott_id" = ".id"))

taxonomy_clean <- na.omit(taxonomy_clean)

DBGI_database <- taxonomy_clean %>% 
                             select("unique_name","name.genus","name.family","name.order","name.class","name.domain")

DBGI_tree <- collapsibleTree(
  DBGI_database,
  hierarchy = c("name.domain","name.class","name.order","name.family", "name.genus", "unique_name"),
  fill = "darkgreen"
)


DBGI_tree %>% 
  htmlwidgets::saveWidget(file="./data/out/DBGI_tree.html", selfcontained = TRUE)
system('rm -r DBGI_tree_files')