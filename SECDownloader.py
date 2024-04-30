from sec_downloader import Downloader
from sec_downloader.types import RequestedFilings
import os
import pdfkit






class FileOrganizer:
    def __init__(self) -> None:
        pass
    def initialize(self, symbol_name):
        folder_path = os.path.join('downloads', symbol_name)
        self.create_folder_if_not_exists(folder_path)
        return folder_path
    def create_folder_if_not_exists(self, folder_path):
        """
        Check if a folder exists, if not, create it.

        Parameters:
        folder_path (str): Path to the folder to be checked/created.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            pass

class SecDownloader:
    def __init__(self, company_name = "JnanMarga Technologies", email = "prajwal@jnanamarga.in") -> None:
        self.dl = Downloader(company_name, email)
        self.fo = FileOrganizer()
    def download_past_n_filings(self, symbol, form_type = '10-K', n = 1):
        metadatas_as_dict = []
        try:
            metadatas = self.dl.get_filing_metadatas( RequestedFilings(ticker_or_cik=symbol, form_type=form_type, limit=n))
            metadatas_as_dict = [i.__dict__ for i in metadatas]
        except Exception as e:
            print("The symbol is incorrect", str(e))
        
        return metadatas_as_dict
    def convert_url_to_pdf(self, url, output_file):
        try:
            # Convert URL to PDF
            pdfkit.from_url(url, output_file)
        except Exception as e:
            print(f"An error occurred: {e}") 
    def get_pdf_of_symbol(self, symbol, form_type = '10-K', n = 1):
        #Get the required pdf first
        all_file_paths = []
        metadatas = self.download_past_n_filings(symbol=symbol, form_type=form_type, n = n)

        if metadatas:
            folder_path = self.fo.initialize(symbol )

            #Initialize the form_type folder

            form_folder = os.path.join(folder_path, form_type)
            self.fo.create_folder_if_not_exists(form_folder)
            

            #Save the files now
            for file in metadatas:
                file_name = os.path.join(form_folder, file.get("accession_number", file.get("report_date")) + ".pdf")
                self.convert_url_to_pdf(file.get("primary_doc_url", ""), file_name)
                all_file_paths.append(file_name)

        return all_file_paths


if __name__ == "__main__":
    sec = SecDownloader()
    out = sec.get_pdf_of_symbol('NFLX')
    print(out)

        




    
    

    