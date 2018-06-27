import remi.gui as gui
from remi import start, App
import pypandoc
import pathlib
from xhtml2pdf import pisa
import urllib.request as urllib2


class MyApp(App):
    #Input:
    def __init__(self, *args):
        impath = str(pathlib.Path('.').absolute())
        super(MyApp, self).__init__(*args, static_file_path=impath)

    def main(self):
        verticalContainer = gui.Widget(width=800, margin='0px auto',
                                           style={'display': 'block', 'overflow': 'hidden'})
        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px',
                                         style={'display': 'block', 'overflow': 'auto'})
        subContainerLeft = gui.Widget(width=300,
                                          style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        subContainerRight = gui.Widget(width=500,
                                      style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})

        self.txt_subject = gui.TextInput(width=150, height=35, margin='10px')
        self.txt_subject.set_text("Subject number")
        self.txt_subject.style['font-size'] = '16px'
        self.txt_subject.style['background'] = 'lightblue'

        self.date_headline = gui.Label('Acquisition date:', width=150, height=20, margin='10px')
        self.date = gui.Date('2018-01-01', width=150, height=30, margin='10px')


        self.txt = gui.TextInput(width=250, height=50, margin='10px')
        self.txt.set_text('Add remarks here')

        self.table = gui.Table.new_from_list([['Region', 'value', 'Z-score'],
                                              ['Prefrontal Lateral R', '80', '1.2'],
                                              ['Prefrontal Lateral L', '25', '1.99'],
                                              ['Sensorimotor R', '76', '0.23'],
                                              ['Sensorimotor L', '88', '2.55']], width=250, height=500, margin='10px')


        subContainerLeft.append([self.txt_subject,  self.date_headline, self.date, self.txt, self.table])
        self.bt_analyze = gui.Button("Analyze", width=300, height=30, margin='10px')
        #self.bt_analyze.onclick.connect(self.on_analyze_pressed)

        self.figure_analyzed = gui.Image(r'/res/es.jpg', width=300, height=300, margin='10px')
        subContainerRight.append([self.bt_analyze, self.figure_analyzed])
        self.sub_container_left = subContainerLeft
        self.sub_container_right = subContainerRight

        horizontalContainer.append([self.sub_container_left, self.sub_container_right])

        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Select Subject', width=100, height=30)
        m1.onclick.connect(self.menu_subject_clicked)
        m2 = gui.MenuItem('Properties', width=100, height=30)
        m3 = gui.MenuItem("Export as", width=100, height=30)
        m21 = gui.MenuItem('Select Mask', width=200, height=30)
        m21.onclick.connect(self.menu_mask_clicked)
        m22 = gui.MenuItem('General population data', width=200, height=30)
        m31 = gui.MenuItem('PDF', width=100, height=30)
        m31.onclick.connect(self.menu_pdf_clicked)
        m221 = gui.MenuItem('Select mean data', width=100, height=30)
        m221.onclick.connect(self.menu_mean_clicked)
        m222 = gui.MenuItem('Select SD data', width=100, height=30)
        m222.onclick.connect(self.menu_sd_clicked)
        m223 = gui.MenuItem('Select template', width=100, height=30)
        m223.onclick.connect(self.menu_template_clicked)
        menu.append([m1, m2, m3])
        m2.append([m21, m22])
        m3.append([m31])
        m22.append([m221, m222, m223])

        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        verticalContainer.append([menubar, horizontalContainer])

        return verticalContainer

    def on_analyze_pressed(self, widget):
        self.figure_analyzed = gui.Image(self.fileselectionDialog)

        self.sub_container_right.append(self.figure_analyzed)


    def menu_subject_clicked(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', "Select subject's map file", False,
                                                           '.')
        self.fileselectionDialog.confirm_value.connect(self.on_subject_fileselection_dialog_confirm)
        self.fileselectionDialog.show(self)

    def on_subject_fileselection_dialog_confirm(self, widget, filelist):
        """ Called when the user pressed 'Done' in the
        file selection dialog """
        self.map_file = filelist[0]

    def menu_mask_clicked(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.confirm_value.connect(self.on_mask_fileselection_dialog_confirm)
        self.fileselectionDialog.show(self)

    def on_mask_fileselection_dialog_confirm(self, widget, filelist):
        """ Called when the user pressed 'Done' in the
        file selection dialog """
        self.mask_file = filelist[0]

    def menu_mean_clicked(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.confirm_value.connect(self.on_mean_fileselection_dialog_confirm)
        self.fileselectionDialog.show(self)

    def on_mean_fileselection_dialog_confirm(self, widget, filelist):
        """ Called when the user pressed 'Done' in the
        file selection dialog """
        self.mean_file = filelist[0]

    def menu_sd_clicked(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.confirm_value.connect(self.on_sd_fileselection_dialog_confirm)
        self.fileselectionDialog.show(self)

    def on_sd_fileselection_dialog_confirm(self, widget, filelist):
        """ Called when the user pressed 'Done' in the
        file selection dialog """
        self.sd_file = filelist[0]

    def menu_template_clicked(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.confirm_value.connect(self.on_template_fileselection_dialog_confirm)
        self.fileselectionDialog.show(self)

    def on_template_fileselection_dialog_confirm(self, widget, filelist):
        """ Called when the user pressed 'Done' in the
        file selection dialog """
        self.template_file = filelist[0]


    def menu_pdf_clicked(self, widget):
        url = urllib2.urlopen('http://127.0.0.1:8081')
        sourceHtml = url.read()
        pisa.showLogging()
        outputFilename = "test555.pdf"
        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(sourceHtml, resultFile)
        resultFile.close()

if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    #import ssl

    start(MyApp, debug=True, address='127.0.0.1', start_browser=True, multiple_instance=True)




