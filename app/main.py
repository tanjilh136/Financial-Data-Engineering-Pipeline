from steeleye_assignment.downloader import Downloader
from steeleye_assignment.index_parser import IndexParser
from steeleye_assignment.extractor import Extractor
from steeleye_assignment.dltins_parser import DLTINSParser
from steeleye_assignment.enricher import DataEnricher
from steeleye_assignment.csv_writer import CSVWriter


if __name__ == "__main__":
    index_url = (
        "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?"
        "q=*&fq=publication_date:[2021-01-17T00:00:00Z TO 2021-01-19T23:59:59Z]&wt=xml"
        "&indent=true&start=0&rows=100"
    )

    # Step 1: Download index.xml
    downloader = Downloader()
    index_path = downloader.download_file(index_url, "index.xml")

    # Step 2: Extract second DLTINS link
    index_parser = IndexParser(index_path)
    dltins_url = index_parser.get_second_dltins_url()

    if dltins_url:
        # Step 3: Download DLTINS ZIP
        zip_path = downloader.download_file(dltins_url)

        # Step 4: Extract XML from ZIP
        extractor = Extractor()
        extracted_xml = extractor.extract_xml(zip_path)

        print(f"\n➡️ Extracted XML path: {extracted_xml}\n")

        # Step 5: Parse XML to DataFrame
        dltins_parser = DLTINSParser(extracted_xml)
        df = dltins_parser.parse_to_dataframe()

        if df is not None:
            # Step 6: Enrich the DataFrame
            enricher = DataEnricher(df)
            df = enricher.enrich()

            # Step 7: Save to CSV
            csv_writer = CSVWriter()
            csv_path = csv_writer.save_to_csv(df)

            if csv_path:
                print(f"\n✅ CSV saved at: {csv_path}")
            else:
                print("\n❌ Failed to save CSV")
        else:
            print("\n❌ Failed to parse XML into DataFrame")
    else:
        print("\n❌ Second DLTINS URL not found in index file")
