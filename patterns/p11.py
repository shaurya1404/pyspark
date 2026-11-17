# Explode Array/Struct Columns (Medium)

# Problem
# Each article stores its tags as a single comma-separated string, which makes tag-level reporting impossible. 
# Produce a normalized list that has one row per article-tag pair. 
# For every tag attached to an article, output the article's article_id, its title, the individual tag, and its publish_date.

# List the rows ordered by article_id, and within each article order the tags alphabetically.

# Input columns: article_id, title, tags, publish_date
# Output columns: article_id, title, tag, publish_date

# Order the result by article_id.

from pyspark.sql import functions as F

def exploded(articles):
    return (
        articles.withColumn('tag', F.explode(F.split(F.col('tags'), ','))).withColumn('tag', F.trim('tag')) # Using .trim() as a saftey net for erroneous whitespaces
            .select('article_id', 'title', 'tag', 'publish_date').orderBy('article_id', 'tag')
    )

# Note: Using .select() instead of .drop() to re-order the columns as well in accordance to the expected output