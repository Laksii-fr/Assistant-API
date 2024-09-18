import ocrmypdf
import asyncio
from app.utils.utils import get_file_name


async def convert_pdf_to_text(filepath, input_local_directory, output_local_directory, sidecar_local_directory):
        filename = get_file_name(filepath)
        # ocr_input_file = input_local_directory + '/' + filename + '.pdf'
        # ocr_output_file = output_local_directory + '/' + filename + '_ocr.pdf'
        # ocr_sidecar_file = sidecar_local_directory + '/' + filename + '_ocr.txt'
        ocr_input_file = input_local_directory + filename + '.pdf'
        ocr_output_file = output_local_directory + filename + '_ocr.pdf'
        ocr_sidecar_file = sidecar_local_directory + filename + '_ocr.txt'
        await async_ocr(ocr_input_file, ocr_output_file, ocr_sidecar_file)
        return ocr_output_file, ocr_sidecar_file


async def async_ocr(ocr_input_file, ocr_output_file, ocr_sidecar_file):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None,
                                            lambda: ocrmypdf.ocr(ocr_input_file, ocr_output_file, output_type=None,
                                                          force_ocr=True, sidecar=ocr_sidecar_file))

        return result
