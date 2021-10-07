from markdown import markdown

def md_to_html(fn, target_dir, output_fn):
    print("Running input through markdown conversion....")
    with open(fn, 'r') as f:
        text = f.read()
        html = markdown(text)
    with open(f'{target_dir}/{output_fn}', 'w') as f:
        f.write(html)
