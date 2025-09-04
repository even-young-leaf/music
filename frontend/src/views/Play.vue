<template>
  <div class="play-page">
    <div class="song-info">
      <div class="song-cover">
        <img :src="song.img || '/static/image/default_cover.jpg'" alt="封面">
      </div>
      
      <div class="song-details">
        <h1>{{ song.name }}</h1>
        <p class="singer">歌手：{{ song.singer }}</p>
        <p class="album">专辑：{{ song.album }}</p>
        <p class="release">发行日期：{{ song.release }}</p>
        <p class="language">语种：{{ song.language }}</p>
        <p class="type">类型：{{ song.type }}</p>
        
        <div class="song-stats">
          <span class="stat">播放：{{ song.plays || 0 }}</span>
          <span class="stat">下载：{{ song.downloads || 0 }}</span>
          <span class="stat">搜索：{{ song.searches || 0 }}</span>
        </div>
        
        <div class="song-actions">
          <button class="action-btn play" @click="togglePlay">
            {{ isPlaying ? '暂停' : '播放' }}
          </button>
          <button class="action-btn download" @click="downloadSong">
            下载
          </button>
          <button class="action-btn add-to-list" @click="addToPlaylist">
            加入播放列表
          </button>
        </div>
      </div>
    </div>
    
    <div class="player-container">
      <audio 
        ref="audioPlayer" 
        :src="song.file" 
        @play="onPlay" 
        @pause="onPause"
        @ended="onEnded"
        @timeupdate="onTimeUpdate"
        controls>
        您的浏览器不支持音频播放
      </audio>
      
      <div class="progress-bar">
        <div class="progress" :style="{width: progress + '%'}"></div>
      </div>
      
      <div class="time-info">
        <span>{{ formatTime(currentTime) }}</span>
        <span>{{ formatTime(duration) }}</span>
      </div>
    </div>
    
    <div class="lyrics-container" v-if="lyrics">
      <h2>歌词</h2>
      <div class="lyrics">
        <pre>{{ lyrics }}</pre>
      </div>
    </div>
    
    <div class="comments-section">
      <h2>评论 ({{ comments.length }})</h2>
      
      <div class="comment-form" v-if="isLoggedIn">
        <textarea 
          v-model="newComment" 
          placeholder="发表您的评论..."
          rows="3"></textarea>
        <button @click="submitComment">提交评论</button>
      </div>
      <div class="login-prompt" v-else>
        <router-link to="/user/login">登录</router-link> 后才能发表评论
      </div>
      
      <div class="comments-list">
        <div class="comment" v-for="comment in comments" :key="comment.id">
          <div class="comment-header">
            <span class="comment-user">{{ comment.user_name }}</span>
            <span class="comment-time">{{ comment.time }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayPage',
  data() {
    return {
      song: {},
      lyrics: '',
      comments: [],
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      progress: 0,
      newComment: ''
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    }
  },
  created() {
    this.fetchSongData();
  },
  watch: {
    '$route.params.id': function() {
      this.fetchSongData();
    }
  },
  methods: {
    fetchSongData() {
      const songId = this.$route.params.id;
      
      // 获取歌曲信息
      this.$axios.get(`/api/play/${songId}/`)
        .then(response => {
          this.song = response.data.song || {};
          this.lyrics = response.data.lyrics || '';
          this.comments = response.data.comments || [];
          
          // 更新当前播放歌曲
          this.$store.commit('setCurrentSong', this.song);
        })
        .catch(error => {
          console.error('获取歌曲数据失败:', error);
        });
    },
    togglePlay() {
      const player = this.$refs.audioPlayer;
      if (this.isPlaying) {
        player.pause();
      } else {
        player.play();
      }
    },
    downloadSong() {
      if (this.song.file) {
        // 创建下载链接
        const link = document.createElement('a');
        link.href = this.song.file;
        link.download = `${this.song.name} - ${this.song.singer}.mp3`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // 记录下载次数
        this.$axios.post(`/api/song/${this.song.id}/download/`)
          .catch(error => {
            console.error('记录下载失败:', error);
          });
      }
    },
    addToPlaylist() {
      this.$store.commit('addToPlaylist', this.song);
      alert('已添加到播放列表');
    },
    onPlay() {
      this.isPlaying = true;
      // 记录播放次数
      this.$axios.post(`/api/song/${this.song.id}/play/`)
        .catch(error => {
          console.error('记录播放失败:', error);
        });
    },
    onPause() {
      this.isPlaying = false;
    },
    onEnded() {
      this.isPlaying = false;
      this.progress = 0;
    },
    onTimeUpdate() {
      const player = this.$refs.audioPlayer;
      this.currentTime = player.currentTime;
      this.duration = player.duration || 0;
      this.progress = (this.currentTime / this.duration) * 100 || 0;
    },
    formatTime(seconds) {
      if (!seconds) return '00:00';
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    submitComment() {
      if (!this.newComment.trim()) return;
      
      this.$axios.post(`/api/song/${this.song.id}/comment/`, {
        content: this.newComment
      })
        .then(response => {
          // 添加新评论到列表
          this.comments.unshift(response.data);
          this.newComment = '';
        })
        .catch(error => {
          console.error('提交评论失败:', error);
        });
    }
  }
};
</script>

<style scoped>
.play-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.song-info {
  display: flex;
  margin-bottom: 30px;
}

.song-cover {
  width: 200px;
  height: 200px;
  margin-right: 30px;
}

.song-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.song-details {
  flex: 1;
}

.song-details h1 {
  margin-top: 0;
  margin-bottom: 15px;
}

.song-details p {
  margin: 8px 0;
  color: #666;
}

.song-stats {
  margin: 15px 0;
}

.stat {
  margin-right: 15px;
  color: #888;
}

.song-actions {
  margin-top: 20px;
}

.action-btn {
  padding: 8px 16px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.play {
  background-color: #1890ff;
  color: white;
}

.download {
  background-color: #52c41a;
  color: white;
}

.add-to-list {
  background-color: #faad14;
  color: white;
}

.player-container {
  margin-bottom: 30px;
}

audio {
  width: 100%;
  margin-bottom: 10px;
}

.progress-bar {
  height: 6px;
  background-color: #eee;
  border-radius: 3px;
  margin-bottom: 5px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #1890ff;
  border-radius: 3px;
}

.time-info {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.9em;
}

.lyrics-container {
  margin-bottom: 30px;
}

.lyrics {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

.lyrics pre {
  white-space: pre-wrap;
  font-family: inherit;
  margin: 0;
  line-height: 1.6;
}

.comments-section h2 {
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 10px;
}

.comment-form button {
  padding: 8px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-prompt {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  text-align: center;
}

.login-prompt a {
  color: #1890ff;
  text-decoration: none;
}

.comments-list {
  margin-top: 20px;
}

.comment {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-user {
  font-weight: bold;
  color: #1890ff;
}

.comment-time {
  color: #999;
  font-size: 0.9em;
}

.comment-content {
  line-height: 1.5;
}
</style>