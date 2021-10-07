import re
import os

# ---------------------------------------------------------------------
# cleanup the asciidoc
# ---------------------------------------------------------------------

# beautify function
print("Beautifying asciidoc markup...")
def beautify_text(text):
    # don't beautify verse
    if text.find("[verse]\n____") == -1:
        # make sure we can still have literals/code blocks
        #r = re.compile(r'----')
        #text = re.sub(r, r'@@@@', text)
        # em dashese
        #r = re.compile(r'--')
        #text = re.sub(r, r'&#8212;', text)
        # quotes
        r = re.compile(r'"(.*?)"')
        text = re.sub(r, r'"`\1`"', text)
        # return our literals and code blocks
        #r = re.compile(r'@@@@')
        #text = #re.sub(r, r'----', text)
        # return any role markers
        r = re.compile(r'\[role\=\"\`(.*?)\`\"\]')
        text = re.sub(r, r'[role="\1"]', text)
    return text

# check for includes and if so, manage them
# Note to self: wouldn't it be easier just to... include the inclues in the file, and then only run the beautify script once?
def check_includes(fn, target_dir, parentPath=''):
    # get file
    dirs = fn.split("/")
    fnpath = "/".join(dirs[:-1]) + "/"
    parentText = open(fn, 'r').read()

    # check for includes
    p = re.compile(r'include\:\:(.*?).adoc')
    result = p.findall(parentText)
    if len(result) > 0:
        for x in range(len(result)):
            # get relevant information
            childFn = result[x] + ".adoc"
            # check if the child is inside a directory
            childPath = ''
            if len(childFn.split('/')) > 1:
                childPath = "/".join(childFn.split('/')[:-1])
                if os.path.isdir(target_dir + childPath) == False:
                    os.mkdir(target_dir + childPath)
            childFnPath = fnpath + childFn
            childText = open(childFnPath, 'r').read()
            # build the output file to the buildsrc directory
            open(target_dir + parentPath + childFn, 'w').write(beautify_text(childText))
            # check for includes inside in the child include
            check_includes(childFnPath, childPath + '/')
    # return corrected text
    return beautify_text(parentText)


# ---------------------------------------------------------------------
# Asciidoctor step
# ---------------------------------------------------------------------

def asciidoc_to_html(fn, target_dir, output_fn):
    print("Running our input through asciidoctor....")
    try:
        run_adoctor = f"asciidoctor -a stylesheet! {fn} -D {target_dir} -o {output_fn}"
        if os.system(run_adoctor) != 0:
            raise Exception('Error: there was a problem running asciidoctor. Please ensure you have asciidoctor installed on your path.')
    # TO DO:
    # * Better exception handling
    # * Python asciidoc fallback?
    except:
        print("Error: something went wrong while running asciidoctor; please check your configuration.")
