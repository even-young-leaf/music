import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 用户信息
    user: null,
    // 当前播放的歌曲
    currentSong: null,
    // 播放列表
    playlist: []
  },
  mutations: {
    // 设置用户信息
    setUser(state, user) {
      state.user = user
    },
    // 设置当前播放歌曲
    setCurrentSong(state, song) {
      state.currentSong = song
    },
    // 添加歌曲到播放列表
    addToPlaylist(state, song) {
      // 避免重复添加
      if (!state.playlist.some(item => item.id === song.id)) {
        state.playlist.push(song)
      }
    },
    // 清空播放列表
    clearPlaylist(state) {
      state.playlist = []
    }
  },
  actions: {
    // 异步获取用户信息
    async fetchUserInfo({ commit }, userId) {
      try {
        const response = await Vue.prototype.$axios.get(`/api/user/${userId}/`)
        commit('setUser', response.data)
        return response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return null
      }
    }
  },
  getters: {
    // 是否已登录
    isLoggedIn: state => !!state.user,
    // 获取播放列表长度
    playlistCount: state => state.playlist.length
  }
})