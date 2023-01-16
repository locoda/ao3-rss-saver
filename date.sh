for f in exports/*/*.html 
do
    tmp=$(grep -E "Published: (\d\d\d\d-\d\d-\d\d)" "$f" | awk '{print $2}')
    ext='T00:00:00'
    touch -d "$tmp$ext" "$f"
done