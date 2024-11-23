<template>
  <span :title="fullAddress">{{ showFull ? fullAddress : shortenedAddress }}</span>
</template>

<script>
export default {
  name: "Address",
  props: {
    address: {
      type: String,
      required: true,
    },
    maxLength: {
      type: Number,
      default: 12,
    },
    showFull: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    fullAddress() {
      return this.address;
    },
    shortenedAddress() {
      if (!this.address) {
        return "";
      }
      if (this.address.length <= this.maxLength) {
        return this.address;
      }

      const start = this.address.substring(0, 6);
      const end = this.address.slice(-4);

      return `${start}...${end}`;
    },
  },
};
</script>
