<template>
  <router-view v-slot="{ Component, route }">
    <transition name="fade" mode="out-in">
      <keep-alive>
        <component
          :is="Component"
          class="container"
          :class="'tab-' + route.name"
        />
      </keep-alive>
    </transition>
  </router-view>
</template>