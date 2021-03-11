from library import *import cv2#one file#mode = {'in_files': ['A3.pdf'],#        'save_out_fig':True}#list of files:#mode = {'in_files': ['A3.pdf', 'D4.pdf'],#        'save_out_fig':True}# for all files in foldermode = {'save_out_img_noCoord':True,        'save_out_img_Coord': True,        'show_conturs':False,        'show_process':True,        'in_files': ['all'],        'noise_removal_threshold' : 10000, # minimal area of a room in pix ~5000-10000        'k_approxPolyDP': 0.02            # koeff for approxPolyDP procedure ~0.02        }class settings(object):    '''    set settings    '''    def __init__(self, mode):        #working mode        self.mode = mode        # folder for input (JPEG/JPG, BMP, PDF, PNG, DWG) files        self.input_img_folder_rel = 'Input_img/'        # folder for output files        self.out_folder_main_rel = 'Out/'        self.input_img_folder = path_abs_make(self.input_img_folder_rel)        self.out_folder_main = path_abs_make(self.out_folder_main_rel)        #out files:        #out image no coordinates        self.out_folder_img_noCoord = os.path.join(self.out_folder_main, 'Out_img_noCoord/')        # out image with coordinates        self.out_folder_img_coord = os.path.join(self.out_folder_main, 'Out_img_Coord/')        #out json        self.out_folder_json = os.path.join(self.out_folder_main, 'Out_json/')        if mode['in_files'] != 'all':            #make a list of '.pdf', '.jpeg', '.jpg', '.bmp', '.png' files            self.in_files = create_list_of_files_in_formats(self.input_img_folder)            #self.in_files = create_list_of_pdf(self.input_img_folder) #.pdf only        else:            self.in_files = mode['in_files']        self.save_out_img_noCoord = self.mode['save_out_img_noCoord']        self.save_out_img_Coord = self.mode['save_out_img_Coord']        self.show_conturs = self.mode['show_conturs']        self.show_process = self.mode['show_process']        # minimal area of a room in pix        self.noise_removal_threshold = self.mode['noise_removal_threshold']        self.k_approxPolyDP = self.mode['k_approxPolyDP']class find_count_v2():    def __init__(self, SET, img_file_name):        '''        :param img_file_name: .pdf or .png        :param out_folder_name:        '''        #input files        self.input_img_folder = SET.input_img_folder        self.img_file_name = img_file_name  # image .pdf file        #output files        self.out_folder_img_noCoord = SET.out_folder_img_noCoord             # out image no coordinates        self.out_folder_img_coord = SET.out_folder_img_coord # out image with coordinates        # out json        self.out_folder_json = SET.out_folder_json        self.out_json_file = '%s%s.txt' % (self.out_folder_json, replce_format_from_file_name(self.img_file_name))        #out figures        self.save_out_img_noCoord = SET.save_out_img_noCoord        self.save_out_img_Coord = SET.save_out_img_Coord        self.show_conturs = SET.show_conturs        self.show_process = SET.show_process        # paramerers for the contour approximation (smoothing)        self.k_approxPolyDP = SET.k_approxPolyDP        # minimal area of a room in pix        self.noise_removal_threshold = SET.noise_removal_threshold        #read image (.pdf or .jpeg/.jpg, .bmp, .png)        self.img_rgb = load_image(self.input_img_folder + self.img_file_name)        # an image transformation to make it easier to find contours        self.img_go = image_transform2find_contours(self.img_rgb)        #to find rooms on a figure using cv2.findContours        self.corner_coordinates = self.find_rooms(self.noise_removal_threshold, self.show_conturs)        #Out:        #save json        save_out_dict(self.corner_coordinates, self.out_json_file)        # save the transformed image to file        #if self.save_out_img_noCoord == True:        #    save_test_image(self.out_folder_img_noCoord, self.img_file_name, self.img_go, 'go')        # save the input image to file        if self.save_out_img_noCoord == True:            save_test_image(self.out_folder_img_noCoord, self.img_file_name, self.img_go, 'in')            #save_test_image(self.out_folder_img_noCoord, self.img_file_name, self.img_rgb, 'in')        #save figure  with coordinates        if self.save_out_img_Coord == True:            draw_main_out_figure(self.img_rgb, self.corner_coordinates,                                 self.out_folder_img_coord, self.img_file_name,                                 self.show_process)    def find_rooms(self, noise_removal_threshold, show_conturs):        '''        to find rooms on a figure using cv2.findContours        : param noise_removal_threshold - minimal area of a room in pix (~5000)        :return:        '''        # find the contours        contours, hierarchy = cv2.findContours(self.img_go, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)        # find the contours 'bigger' then the minimal area in pixel (see noise_removal_threshold)        contours = choose_big_conturs(contours, noise_removal_threshold)        # approximate (smooth) the contour and to return as dictionary:        #{N_room: [[x1, y1], [x2, y2],..], ..}        corner_coordinates, contours_smooth = return_contours_as_poligon(contours.copy(),                                                                         self.k_approxPolyDP)        #test figure for contours -->        if show_conturs == True:            draw_conturs(contours_smooth, self.img_rgb.copy(), True, False)        return corner_coordinatesdef for_all_pdf_files_in_list(SET):    '''    :param SET:    :return:    '''    #if there are files in the input folder    if len(SET.in_files) == 0:        print('Tere is no files in the input folder')        raise SystemExit(1)    #for all files in SET.in_files list    for img_file_name in SET.in_files:        print('In file: %s' % (img_file_name))        CONTORS = find_count_v2(SET, img_file_name)        #try:        #    CONTORS = find_count_v2(SET, img_file_name)        #except:        #    print('There is problems with %s file'%img_file_name)if __name__ == '__main__':    SET = settings(mode)    for_all_pdf_files_in_list(SET)