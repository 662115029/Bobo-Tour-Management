<template>
  <div class="flex flex-col items-center justify-between fixed inset-0 bg-white py-16 z-50">
    <div/>
    <div class="flex flex-col items-center gap-5">
      <div class="bobo-bear">
        <img :src="boboLogo" alt="Bobo" class="w-32 h-32 object-contain drop-shadow-lg" />
      </div>
      <div class="text-center">
        <h1 class="text-xl font-black text-gray-900 tracking-tight">BOBO BOT</h1>
        <p class="text-xs text-gray-400 mt-1">{{ message }}</p>
      </div>
    </div>
    <div class="flex flex-col items-center gap-3 pb-4">
      <div class="flex items-center gap-2">
        <span class="loading-dot" style="background:#dc2626; animation-delay: 0ms"/>
        <span class="loading-dot" style="background:#dc2626; opacity:0.6; animation-delay: 150ms"/>
        <span class="loading-dot" style="background:#dc2626; opacity:0.3; animation-delay: 300ms"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import boboLogo from '@/assets/logo.png'
defineProps({ message: { type: String, default: 'Loading...' } })
</script>

<style scoped>
.bobo-bear {
  animation: bobo-breathe 2.5s ease-in-out infinite;
  transform-origin: bottom center;
}
@keyframes bobo-breathe {
  0%   { transform: scale(1)    translateY(0px); }
  25%  { transform: scale(1.04) translateY(-4px); }
  50%  { transform: scale(1.06) translateY(-6px); }
  75%  { transform: scale(1.04) translateY(-4px); }
  100% { transform: scale(1)    translateY(0px); }
}
.loading-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: dot-bounce 1s ease-in-out infinite;
}
@keyframes dot-bounce {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-6px); }
}
</style>