<template>
    <div class="fixed top-6 right-6 z-[100] flex flex-col gap-2">
        <transition-group name="toast">
            <div v-for="t in toasts" :key="t.id"
                class="flex items-center gap-2.5 px-4 py-3 rounded-xl shadow-lg text-sm font-medium min-w-[260px] max-w-sm"
                :class="t.type === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'">
                <svg v-if="t.type === 'success'" class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none"
                    stroke="white" stroke-width="2.5">
                    <path d="M20 6L9 17l-5-5" />
                </svg>
                <svg v-else class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="white"
                    stroke-width="2.5">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {{ t.message }}
            </div>
        </transition-group>
    </div>
</template>
<script setup>
import { useToast } from './useToast.js'
const { toasts } = useToast()
</script>
<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
    opacity: 0;
    transform: translateX(20px);
}
</style>