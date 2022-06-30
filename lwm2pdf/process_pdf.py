import os
import subprocess
import shutil
from weasyprint import HTML, CSS  # type: ignore
from weasyprint.fonts import FontConfiguration  # type: ignore


def open_pdf(output_fn, ask):
    """
    helper function to try and open the pdf; in theory cross-platform
    but I haven't really done much testing on this.
    """
    if ask == 'y':
        ask_to_open = 'y'
    elif ask == 'n':
        ask_to_open = "n"
    else:
        ask_to_open = input('Do you want to open the PDF? [y/n] ')
    if ask_to_open == 'y':
        try:
            try_mac = subprocess.run(['open', output_fn],
                                     capture_output=True, text=True)
            if try_mac.stderr == '':
                return try_mac.stdout
        except FileNotFoundError:
            try:
                try_linux = subprocess.run(['xdg-open', output_fn],
                                           capture_output=True, text=True)
                if try_linux.stderr == '':
                    return try_linux.stdout
            except FileNotFoundError:
                try:
                    try_pc = subprocess.run(['open', output_fn],
                                            capture_output=True, text=True)
                    if try_pc.stderr == '':
                        return try_pc.stdout
                except Exception:
                    print("Sorry, we can't seem to open the file." +
                          "Try opening with your file browser.")


def create_pdf(fn, output_fn, buildfiles_dir, output_html, styles, options):
    """ Build final PDF """
    try:
        font_config = FontConfiguration()
        HTML(output_html).write_pdf(
            output_fn,
            stylesheets=[CSS(string=styles)],
            font_config=font_config)
        # Let the user know where it lives now
        print(f"\nSuccess! A PDF from {fn} has been successfully built" +
              f" and saved to:\n{output_fn}\n")
    except AttributeError as ae:
        print(ae)
    except Exception as unk_e:
        print(f"There was an error building the PDF.\n{Exception}\n{unk_e}")

    # Cleanup build files if they're not wanted
    if not options.save_buildfile and os.path.isdir(buildfiles_dir):
        shutil.rmtree(buildfiles_dir)

    return True
