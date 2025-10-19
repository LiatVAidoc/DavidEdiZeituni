<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>DICOM Metadata Viewer</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <h1 class="text-h4 mb-5">DICOM Metadata Viewer</h1>
        
        <!-- S3 Path Form -->
        <v-card class="mb-5">
          <v-card-title>Enter S3 Path</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="fetchDicomMetadata">
              <v-text-field
                v-model="s3Path"
                label="S3 Path"
                placeholder="bucket-name/path/to/file.dcm"
                :rules="[v => !!v || 'S3 Path is required']"
                required
              ></v-text-field>
              <v-btn
                color="primary"
                type="submit"
                :loading="loading"
                :disabled="loading"
              >
                Fetch Metadata
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <!-- Metadata Display -->
        <v-card v-if="metadata">
          <v-card-title>DICOM Metadata</v-card-title>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th>Tag</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <!-- To be implemented by candidate -->
                <tr v-for="(value, key) in metadata" :key="key">
                  <td>{{ key }}</td>
                  <td>{{ value }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>

        <!-- Error Display -->
        <v-alert
          v-if="error"
          type="error"
          class="mt-4"
        >
          {{ error }}
        </v-alert>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import ApiService from './services/api.js';

export default {
  name: 'App',
  data() {
    return {
      s3Path: '',
      metadata: null,
      loading: false,
      error: null
    };
  },
  methods: {
    async fetchDicomMetadata() {
      if (!this.s3Path) {
        this.error = 'Please enter a valid S3 path';
        return;
      }

      this.loading = true;
      this.error = null;
      this.metadata = null;

      try {
        this.metadata = await ApiService.fetchDicomMetadata(this.s3Path);
      } catch (error) {
        console.error('Error fetching DICOM metadata:', error);
        this.error = error.response?.data?.error || 'Failed to fetch DICOM metadata. Please check the S3 path and try again.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script> 