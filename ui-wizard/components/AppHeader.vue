<script setup lang="ts">
interface HeaderLink {
  label: string;
  href?: string;
  isActive?: boolean;
}

interface Props {
  explorerUrl: string;
}

const props = defineProps<Props>();

const links = computed<HeaderLink[]>(() => [
  {
    label: "Assistant",
    isActive: true,
  },
  {
    label: "Explorer",
    href: props.explorerUrl,
  },
]);
</script>

<template>
  <header class="fixed top-0 left-0 right-0 bg-background z-50 border-b border-highlight/20">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center">
        <img src="/intelligent-oracle-logo.svg" alt="Intelligent Oracle" class="h-8" />
      </div>
      <nav class="flex items-center gap-8">
        <template v-for="link in links" :key="link.label">
          <span v-if="link.isActive" class="text-primary-text font-bold">
            {{ link.label }}
          </span>
          <a
            v-else
            :href="link.href"
            target="_blank"
            class="text-secondary-text hover:text-primary-text transition-colors"
          >
            {{ link.label }}
          </a>
        </template>
      </nav>
    </div>
  </header>
</template>
