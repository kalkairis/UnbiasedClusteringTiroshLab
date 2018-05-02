import sys

if __name__=='__main__':
    filename = sys.argv[1]
    print(filename)
    with open(filename, 'r') as html_file:
         content = html_file.read()
    content = content.replace("div.input_area {", "div.input_area {\n\tdisplay: none;")
    content = content.replace(".prompt {", ".prompt {\n\tdisplay: none;")

    f = open(filename, 'w')
    f.write(content)
    f.close()

