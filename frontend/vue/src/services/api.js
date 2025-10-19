import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

class ApiService {
  /**
   * Fetch DICOM metadata from the server
   * @param {string} filePath - The S3 file path
   * @returns {Promise} - The API response
   */
  async fetchDicomMetadata(filePath) {
    try {
      const response = await axios.post(`${API_BASE_URL}/dicom-metadata`, {
        file_path: filePath
      });
      return response.data;
    } catch (error) {
      // Re-throw the error to be handled by the component
      throw error;
    }
  }
}

export default new ApiService();