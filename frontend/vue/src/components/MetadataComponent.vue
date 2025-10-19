<template>
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
          <tr
            v-for="(value, key) in metadata"
            :key="key"
          >
            <td>{{ key }}</td>
            <td>{{ value }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'MetadataComponent',
  props: {
    metadata: {
      type: Object,
      default: null
    }
  }
};
</script>