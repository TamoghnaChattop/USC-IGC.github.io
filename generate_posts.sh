for file in `ls __blog/*`
do
    new_file=${file:2:${#file}-4}
    new_file=`echo "$new_file"html`

    python __md2html/md2html.py $file -t "$new_file" \
        --template __md2html/static/html/blog_template.html \
        --css blog.css  --js active-view.js --md_folder __blog
done

# generate all posts page
python __md2html/all_post.py --folder __blog --template __md2html/static/html/all_posts.html --output blog/index.html
