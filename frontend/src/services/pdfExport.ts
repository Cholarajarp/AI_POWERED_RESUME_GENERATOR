import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

export interface PDFExportOptions {
  filename?: string;
  format?: 'A4' | 'Letter';
  quality?: number;
  marginTop?: number;
  marginRight?: number;
  marginBottom?: number;
  marginLeft?: number;
}

export const pdfExportService = {
  /**
   * Export HTML element to PDF
   */
  exportElementToPDF: async (
    element: HTMLElement,
    options: PDFExportOptions = {}
  ): Promise<void> => {
    const {
      filename = 'document.pdf',
      format = 'A4',
      quality = 2,
      marginTop = 10,
      marginRight = 10,
      marginBottom = 10,
      marginLeft = 10,
    } = options;

    try {
      const canvas = await html2canvas(element, {
        scale: quality,
        useCORS: true,
        logging: false,
      });

      const imgData = canvas.toDataURL('image/png');
      const pageWidth = format === 'A4' ? 210 : 215.9;
      const pageHeight = format === 'A4' ? 297 : 279.4;

      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: format,
      });

      const imgWidth = pageWidth - marginLeft - marginRight;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = marginTop;

      pdf.addImage(imgData, 'PNG', marginLeft, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight + marginTop;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', marginLeft, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save(filename);
    } catch (error) {
      console.error('PDF export failed:', error);
      throw new Error('Failed to export PDF');
    }
  },

  /**
   * Export resume to PDF with premium template
   */
  exportResumeToPDF: async (
    resumeContent: string,
    templateType: 'modern' | 'classic' | 'minimal' = 'modern',
    filename: string = 'resume.pdf'
  ): Promise<void> => {
    const pdf = new jsPDF();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 15;
    const maxWidth = pageWidth - 2 * margin;
    let yPosition = margin;

    // Helper function to add wrapped text
    const addWrappedText = (text: string, fontSize: number, isBold: boolean = false) => {
      pdf.setFontSize(fontSize);
      pdf.setFont(undefined, isBold ? 'bold' : 'normal');
      const lines = pdf.splitTextToSize(text, maxWidth);
      pdf.text(lines, margin, yPosition);
      yPosition += (lines.length * fontSize) / 2.5;

      if (yPosition > pageHeight - margin) {
        pdf.addPage();
        yPosition = margin;
      }
    };

    // Add header with name and title
    addWrappedText('Your Name', 20, true);
    addWrappedText('Professional Title', 12);

    // Add contact info
    addWrappedText('email@example.com | (123) 456-7890 | linkedin.com/in/yourprofile', 10);

    // Add separator
    yPosition += 5;
    pdf.setDrawColor(200, 200, 200);
    pdf.line(margin, yPosition, pageWidth - margin, yPosition);
    yPosition += 5;

    // Add content based on template type
    if (templateType === 'modern') {
      addWrappedText('Professional Summary', 14, true);
      addWrappedText(resumeContent, 11);
    } else if (templateType === 'classic') {
      addWrappedText('PROFESSIONAL SUMMARY', 14, true);
      addWrappedText(resumeContent, 10);
    } else {
      addWrappedText('About', 12, true);
      addWrappedText(resumeContent, 10);
    }

    pdf.save(filename);
  },

  /**
   * Export cover letter to PDF
   */
  exportCoverLetterToPDF: async (
    content: string,
    recipientName: string = 'Hiring Manager',
    filename: string = 'cover-letter.pdf'
  ): Promise<void> => {
    const pdf = new jsPDF();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 20;
    const maxWidth = pageWidth - 2 * margin;
    let yPosition = margin;

    // Add date
    const today = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
    pdf.setFontSize(10);
    pdf.text(today, margin, yPosition);
    yPosition += 15;

    // Add recipient
    pdf.setFontSize(11);
    pdf.text(`Dear ${recipientName},`, margin, yPosition);
    yPosition += 10;

    // Add content
    const lines = pdf.splitTextToSize(content, maxWidth);
    pdf.setFontSize(11);
    pdf.text(lines, margin, yPosition);
    yPosition += (lines.length * 11) / 2.5 + 10;

    // Add signature
    pdf.text('Sincerely,', margin, yPosition + 10);
    yPosition += 25;
    pdf.text('Your Name', margin, yPosition);

    pdf.save(filename);
  },
};

export default pdfExportService;
