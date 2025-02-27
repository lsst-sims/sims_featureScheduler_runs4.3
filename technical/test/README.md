Do a quick look at 1 and 3 years




```
rm maf.sh

ls *yrs.db | xargs -I'{}' echo "scimaf_dir --db '{}'" > maf.sh
ls *yrs.db | xargs -I'{}' echo "glance_dir --db '{}'" >> maf.sh
ls *yrs.db | xargs -I'{}' echo "ddf_dir --db '{}'" >> maf.sh
ls *yrs.db | xargs -I'{}' echo "metadata_dir --db '{}'" >> maf.sh

generate_ss
cat ss_script.sh >> maf.sh

cat maf.sh | parallel -j 7
```