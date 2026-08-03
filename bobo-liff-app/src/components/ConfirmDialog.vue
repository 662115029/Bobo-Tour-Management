<template>
    <transition name="dialog-fade">
        <div v-if="isOpen"
            class="fixed inset-0 z-[110] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
            @click.self="handleCancel">
            <transition name="dialog-pop" appear>
                <div v-if="isOpen" class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">
                    <div class="px-6 pt-6 pb-2 flex flex-col items-center text-center">
                        <div class="w-12 h-12 rounded-full bg-amber-50 flex items-center justify-center mb-3">
                            <svg class="w-6 h-6 text-amber-500" fill="none" stroke="currentColor" stroke-width="2"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 9v3.75m0 3.75h.007v.008H12v-.008zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 class="text-[15px] font-bold text-gray-900 mb-1.5">{{ title }}</h3>
                        <p class="text-[13px] text-gray-500 leading-relaxed">{{ message }}</p>
                    </div>
                    <div class="flex gap-2 px-6 pb-6 pt-4">
                        <button @click="handleCancel"
                            class="flex-1 px-4 py-2.5 text-[13px] font-semibold rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 transition">Cancel</button>
                        <button @click="handleConfirm"
                            class="flex-1 px-4 py-2.5 text-[13px] font-semibold rounded-xl bg-red-600 text-white hover:bg-red-700 transition shadow-sm">Continue</button>
                    </div>
                </div>
            </transition>
        </div>
    </transition>
</template>
<script setup>
import { useConfirm } from './useConfirm.js'
const { isOpen, message, title, handleConfirm, handleCancel } = useConfirm()
</script>
<style scoped>
.dialog-fade-enter-active,
.dialog-fade-leave-active {
    transition: opacity 0.2s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
    opacity: 0;
}

.dialog-pop-enter-active {
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.dialog-pop-leave-active {
    transition: all 0.15s ease;
}

.dialog-pop-enter-from {
    opacity: 0;
    transform: scale(0.9) translateY(10px);
}

.dialog-pop-leave-to {
    opacity: 0;
    transform: scale(0.95);
}
</style>