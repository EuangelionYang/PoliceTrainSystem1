<template>
  <div class="app-container">
    <h2 style="text-align: center">发布新课程</h2>
    <!--    训练简介区域-->
    <el-card>
      <div class="course-label">
        <div class="leftImg">
          <img :src="lessonBrief.cover" class="imgStyle" alt="课程封面">
        </div>
        <div class="rightCon">
          <p class="title">{{ lessonBrief.TrainingName }}</p>
          <p class="teacher">
            <span style="padding-right: 20px">
              <svg-icon icon-class="teacher" name="mingcheng"/>
              {{ lessonBrief.teacher_name }}
            </span>
            <span style="padding-left: 20px ">
              <svg-icon icon-class="people" name="number"/>
              {{ lessonBrief.learner_number }}
            </span>
          </p>
          <p class="info">{{ lessonBrief.detail || '暂无简介' }}</p>
        </div>
      </div>
    </el-card>
    <el-button type="text" @click="openChapterDialog">添加课程视频</el-button>
    <!-- 章节 -->
    <ul class="chapterList">
      <li
        v-for="chapter in chapterVideoList"
        :key="chapter.id"
      >
        <p>
          {{ chapter.chapterTitle }}
          <span class="acts">
            <!--<el-button style="" type="text" @click="openVideo(chapter.id)">添加小节</el-button>-->
            <el-button style="" type="text" @click="editChapter(chapter.id)">修改视频</el-button>
            <el-button v-if="lessonType===1" style="" type="text" @click="editResult(chapter.id)">设置参考动作</el-button>
            <el-button v-if="lessonType===2" style="" type="text" @click="editResult(chapter.id)">设置参考情绪</el-button>
            <el-button v-if="lessonType===3" style="" type="text" @click="editResult(chapter.id)">设置参考心理</el-button>
            <el-button v-if="lessonType===4" style="" type="text" @click="editResult(chapter.id)">设置关键帧</el-button>
            <el-button type="text" @click="removeChapter(chapter.id)">删除视频</el-button>
          </span>
        </p>
      </li>
    </ul>
    <div>
      <el-button type="primary" style="float:right; margin:10px 0 20px 20px" @click="publish()">发布课程</el-button>
      <!-- 添加和修改章节表单 -->
      <el-dialog :visible.sync="dialogChapterFormVisible" :title="dialogTitle" @close="handleCancel()">
        <el-form ref="dialogForm" :model="dialogForm" :rules="rules" label-width="80px">
          <el-form-item label="视频标题" prop="chapterTitle">
            <el-input v-model="dialogForm.chapterTitle" placeholder="请输入视频标题"/>
          </el-form-item>
          <el-form-item label="视频编码" prop="chapterID">
            <el-input v-model="dialogForm.chapterID" placeholder="请输入视频编码"/>
          </el-form-item>
          <!-- <el-form-item label="章节排序">
            <el-input-number v-model="dialogForm.sort" :min="0" controls-position="right" />
          </el-form-item> -->
          <el-form-item label="上传视频" prop="chapterFile">
            <el-upload
              :http-request="videoHttpRequest"
              :on-remove="handleVideoRemove"
              :on-exceed="handleUploadExceed"
              :file-list="fileList"
              :limit="1"
              action="#"
              class="upload-demo"
            >
              <el-button size="small" type="primary">上传视频</el-button>
              <el-tooltip placement="right-end">
                <div slot="content">最大支持5G，<br>
                  支持3GP、ASF、AVI、DAT、DV、FLV、F4V、<br>
                  GIF、M2T、M4V、MJ2、MJPEG、MKV、MOV、MP4、<br>
                  MPE、MPG、MPEG、MTS、OGG、QT、RM、RMVB、<br>
                  SWF、TS、VOB、WMV、WEBM 等视频格式上传
                </div>
                <i class="el-icon-question"/>
              </el-tooltip>
            </el-upload>
            <el-progress v-show="progressVisible" :percentage="progress"/>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="handleConfirm()">确 定</el-button>
          <el-button @click="handleCancel()">取 消</el-button>
        </div>
      </el-dialog>
      <!-- 编辑视频内容-->
      <el-dialog :visible="dialogVideoVisible1" title="设置参考动作" width="900px" @close="closeVideoDialog()">
        <el-card>
          <video-player
            ref="videoPlayer"
            :playsinline="true"
            :options="playerOptions"
            class="video-player vjs-custom-skin"
            @play="onPlayerPlay($event)"
            @pause="onPlayerPause($event)"
            @ended="onPlayerEnded($event)"
            @timeupdate="onPlayerTimeupdate($event)"
          />
          <el-button style="" type="text" @click="addResult()">添加参考动作</el-button>
          <el-button style="" type="text" @click="setStartTime()">设置开始时间</el-button>
          <el-button style="" type="text" @click="setEndTime()">设置结束时间</el-button>
          <el-button style="" type="text" @click="skipTime()">跳转到第1秒</el-button>

          <ul class="answer-list">
            <li v-for="item in answerList" :key="item.id" style="margin-bottom:10px">
              <el-form ref="item" :model="item" :rules="answerRules">
                <el-row :gutter="20">
                  <el-col :span="5">
                    <el-form-item prop="start_time">
                      <el-input v-model="item.start_time" :disabled="!item.wait_commit">
                        <template slot="prepend">开始时间</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="end_time">
                      <el-input v-model="item.end_time" :disabled="!item.wait_commit">
                        <template slot="prepend">结束时间</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="4">
                    <el-form-item prop="action">
                      <el-select v-model="item.action" placeholder="参考动作">
                        <!-- <template slot="prepend">动作</template> -->
                        <el-option
                          v-for="ele in actionList"
                          :key="ele.id"
                          :disabled="!item.wait_commit"
                          :label="ele.actionName"
                          :value="ele.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="4">
                    <el-form-item prop="emotion">
                      <el-select v-model="item.emotion" placeholder="参考情绪">
                        <!-- <template slot="prepend">动作</template> -->
                        <el-option
                          v-for="ele in actionList"
                          :key="ele.id"
                          :disabled="!item.wait_commit"
                          :label="ele.actionName"
                          :value="ele.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="4">
                    <el-form-item prop="mood">
                      <el-select v-model="item.mood" placeholder="参考语气">
                        <!-- <template slot="prepend">动作</template> -->
                        <el-option
                          v-for="ele in actionList"
                          :key="ele.id"
                          :disabled="!item.wait_commit"
                          :label="ele.actionName"
                          :value="ele.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="1">
                    <el-button
                      v-if="item.wait_commit"
                      type="primary"
                      icon="el-icon-check"
                      circle
                      size="mini"
                      style="margin-top: 5px"
                      @click="addAnswerList(item)"/>
                    <el-button
                      v-else
                      type="danger"
                      icon="el-icon-close"
                      circle
                      size="mini"
                      style="margin-top: 5px"
                      @click="deleteAnswer(item)"/>
                  </el-col>
                </el-row>
              </el-form>
            </li>
          </ul>
        </el-card>
      </el-dialog>
      <el-dialog :visible="dialogVideoVisible2" title="设置参考情绪" width="900px" @close="closeVideoDialog()">
        <el-card>
          <video-player
            ref="videoPlayer"
            :playsinline="true"
            :options="playerOptions"
            class="video-player vjs-custom-skin"
            @play="onPlayerPlay($event)"
            @pause="onPlayerPause($event)"
            @ended="onPlayerEnded($event)"
            @timeupdate="onPlayerTimeupdate($event)"
          />
          <el-button style="" type="text" @click="addResult()">添加参考情绪</el-button>
          <el-button style="" type="text" @click="setStartTime()">设置开始时间</el-button>
          <el-button style="" type="text" @click="setEndTime()">设置结束时间</el-button>
          <!--          <el-button style="" type="text" @click="skipTime()">跳转到第1秒</el-button>-->

          <ul class="answer-list">
            <li v-for="item in answerList" :key="item.id" style="margin-bottom:10px">
              <el-form ref="item" :model="item" :rules="answerRules">
                <el-row :gutter="20">
                  <el-col :span="5">
                    <el-form-item prop="start_time">
                      <el-input v-model="item.start_time" :disabled="!item.wait_commit">
                        <template slot="prepend">开始</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="end_time">
                      <el-input v-model="item.end_time" :disabled="!item.wait_commit">
                        <template slot="prepend">结束</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <!--                  <el-col :span="4">-->
                  <!--                    <el-form-item prop="action">-->
                  <!--                      <el-select v-model="item.action" placeholder="参考动作">-->
                  <!--                        &lt;!&ndash; <template slot="prepend">动作</template> &ndash;&gt;-->
                  <!--                        <el-option-->
                  <!--                          v-for="ele in actionList"-->
                  <!--                          :key="ele.id"-->
                  <!--                          :disabled="!item.wait_commit"-->
                  <!--                          :label="ele.actionName"-->
                  <!--                          :value="ele.id"-->
                  <!--                        />-->
                  <!--                      </el-select>-->
                  <!--                    </el-form-item>-->
                  <!--                  </el-col>-->
                  <el-col :span="5">
                    <el-form-item prop="emotion">
                      <el-select v-model="item.emotion" placeholder="参考情绪">
                        <!-- <template slot="prepend">动作</template> -->
                        <el-option
                          v-for="ele in actionList"
                          :key="ele.id"
                          :disabled="!item.wait_commit"
                          :label="ele.actionName"
                          :value="ele.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="mood">
                      <el-select v-model="item.mood" placeholder="参考语气">
                        <!-- <template slot="prepend">动作</template> -->
                        <el-option
                          v-for="ele in actionList"
                          :key="ele.id"
                          :disabled="!item.wait_commit"
                          :label="ele.actionName"
                          :value="ele.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="1">
                    <el-button
                      v-if="item.wait_commit"
                      type="primary"
                      icon="el-icon-check"
                      circle
                      size="mini"
                      style="margin-top: 5px"
                      @click="addAnswerList(item)"/>
                    <el-button
                      v-else
                      type="danger"
                      icon="el-icon-close"
                      circle
                      size="mini"
                      style="margin-top: 5px"
                      @click="deleteAnswer(item)"/>
                  </el-col>
                </el-row>
              </el-form>
            </li>
          </ul>
        </el-card>
      </el-dialog>
      <el-dialog :visible="dialogVideoVisible3" title="设置参考心理" width="900px" @close="closeVideoDialog()">
        <el-card>
          <video-player
            ref="videoPlayer"
            :playsinline="true"
            :options="playerOptions"
            class="video-player vjs-custom-skin"
            @play="onPlayerPlay($event)"
            @pause="onPlayerPause($event)"
            @ended="onPlayerEnded($event)"
            @timeupdate="onPlayerTimeupdate($event)"
          />
          <el-button style="" type="text" @click="addResult()">添加参考心理</el-button>
          <el-button style="" type="text" @click="setStartTime()">设置开始时间</el-button>
          <el-button style="" type="text" @click="setEndTime()">设置结束时间</el-button>
          <!--          <el-button style="" type="text" @click="skipTime()">跳转到第1秒</el-button>-->

          <ul class="answer-list">
            <li v-for="item in answerList" :key="item.id" style="margin-bottom:10px">
              <el-form ref="item" :model="item" :rules="answerRules">
                <el-row :gutter="20">
                  <el-col :span="5">
                    <el-form-item prop="start_time">
                      <el-input v-model="item.start_time" :disabled="!item.wait_commit">
                        <template slot="prepend">开始时间</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="end_time">
                      <el-input v-model="item.end_time" :disabled="!item.wait_commit">
                        <template slot="prepend">结束时间</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <!--                  <el-col :span="4">-->
                  <!--                    <el-form-item prop="action">-->
                  <!--                      <el-select v-model="item.action" placeholder="参考动作">-->
                  <!--                        &lt;!&ndash; <template slot="prepend">动作</template> &ndash;&gt;-->
                  <!--                        <el-option-->
                  <!--                          v-for="ele in actionList"-->
                  <!--                          :key="ele.id"-->
                  <!--                          :disabled="!item.wait_commit"-->
                  <!--                          :label="ele.actionName"-->
                  <!--                          :value="ele.id"-->
                  <!--                        />-->
                  <!--                      </el-select>-->
                  <!--                    </el-form-item>-->
                  <!--                  </el-col>-->
                  <el-col :span="4">
                    <el-form-item prop="emotion">
                      <el-select v-model="item.emotion" placeholder="参考心理">
                        <!-- <template slot="prepend">动作</template> -->
                        <el-option
                          v-for="ele in actionList"
                          :key="ele.id"
                          :disabled="!item.wait_commit"
                          :label="ele.actionName"
                          :value="ele.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <!--                  <el-col :span="4">-->
                  <!--                    <el-form-item prop="mood">-->
                  <!--                      <el-select v-model="item.mood" placeholder="参考语气">-->
                  <!--                        &lt;!&ndash; <template slot="prepend">动作</template> &ndash;&gt;-->
                  <!--                        <el-option-->
                  <!--                          v-for="ele in actionList"-->
                  <!--                          :key="ele.id"-->
                  <!--                          :disabled="!item.wait_commit"-->
                  <!--                          :label="ele.actionName"-->
                  <!--                          :value="ele.id"-->
                  <!--                        />-->
                  <!--                      </el-select>-->
                  <!--                    </el-form-item>-->
                  <!--                  </el-col>-->
                  <el-col :span="1">
                    <el-button
                      v-if="item.wait_commit"
                      type="primary"
                      icon="el-icon-check"
                      circle
                      size="mini"
                      style="margin-top: 5px"
                      @click="addAnswerList(item)"/>
                    <el-button
                      v-else
                      type="danger"
                      icon="el-icon-close"
                      circle
                      size="mini"
                      style="margin-top: 5px"
                      @click="deleteAnswer(item)"/>
                  </el-col>
                </el-row>
              </el-form>
            </li>
          </ul>
        </el-card>
      </el-dialog>
      <el-dialog
        :visible="dialogVideoVisible4"
        title="设置关键帧"
        width="900px"
        style="height: auto"
        @close="closeVideoDialog()">
        <el-card height="300px">
          <video-player
            ref="videoPlayer"
            :playsinline="true"
            :options="playerOptions"
            class="video-player vjs-custom-skin"
            @play="onPlayerPlay($event)"
            @pause="onPlayerPause($event)"
            @ended="onPlayerEnded($event)"
            @timeupdate="onPlayerTimeupdate($event)"
          />
          <el-button :disabled="keyframeList.length!==0" type="text" @click="generateKeyframe(videoChapterId)">
            智能生成关键帧
          </el-button>
          <!--          <el-button :disabled="keyframeList.length!==0" type="text" @click="generateKeyframe(videoChapterId)">-->
          <!--            智能生成关键帧-->
          <!--          </el-button>-->
          <el-container
            v-loading="keyframe_loading"
            element-loading-text="正在生成关键帧"
            style="height: 500px">
            <el-aside width="200px">
              <el-card style="min-height: 100%">
                <div slot="header" class="clearfix">
                  <span>关键帧列表</span>
                </div>
                <div v-for="(item,index) of keyframeList" :key="item.id" style="height: auto">
                  <span :class="{active: active_keyframe.id=== item.id}" @click="activeKeyframe(item)">
                    {{
                      '关键帧 ' + index
                    }}</span>
                </div>
              </el-card>
            </el-aside>
            <el-container>
              <el-header height="120px">
                <div>
                  <el-checkbox v-model="checked[0]" :disabled="!active_keyframe.is_edit">左肩</el-checkbox>
                  <el-checkbox v-model="checked[1]" :disabled="!active_keyframe.is_edit">左肘</el-checkbox>
                  <el-checkbox v-model="checked[2]" :disabled="!active_keyframe.is_edit">左腕</el-checkbox>
                  <el-checkbox v-model="checked[3]" :disabled="!active_keyframe.is_edit">左脚</el-checkbox>
                  <el-checkbox v-model="checked[4]" :disabled="!active_keyframe.is_edit">左膝</el-checkbox>
                </div>
                <div>
                  <el-checkbox v-model="checked[5]" :disabled="!active_keyframe.is_edit">右肩</el-checkbox>
                  <el-checkbox v-model="checked[6]" :disabled="!active_keyframe.is_edit">右肘</el-checkbox>
                  <el-checkbox v-model="checked[7]" :disabled="!active_keyframe.is_edit">右腕</el-checkbox>
                  <el-checkbox v-model="checked[8]" :disabled="!active_keyframe.is_edit">右脚</el-checkbox>
                  <el-checkbox v-model="checked[9]" :disabled="!active_keyframe.is_edit">右膝</el-checkbox>
                </div>
              </el-header>
              <el-main style="overflow: hidden">
                <el-input
                  v-model="active_keyframe.keyframe_Description"
                  :rows="11"
                  :disabled="!active_keyframe.is_edit"
                  type="textarea"
                  resize="none"/>
                <div>
                  <el-button
                    :disabled="active_keyframe.id==null"
                    type="danger"
                    style="margin-right: 10px"
                    @click="resetKeyframe">重置
                  </el-button>
                  <el-button :disabled="active_keyframe.id==null" type="primary" @click="submitKeyframe">提交</el-button>
                </div>
              </el-main>
            </el-container>
          </el-container>
        </el-card>
      </el-dialog>

    </div>
  </div>
</template>

<script>
import {getOneTraining, doPublish} from '@/api/lesson/lessonList'
import {
  getChapterList,
  getChapter,
  addChapter,
  updateChapter,
  deleteChapter,
  getChapterPoints,
  getChapterKeyframe, generateChapterKeyframe, editChapterKeyframe
} from '@/api/lesson/chapter'
import {addChapterPoints, deleteChapterPoints} from '@/api/lesson/chapter'
import {getActionList} from '@/api/lesson/action'
// import { uploadByPieces } from '@/utils/upload'
import md5 from 'js-md5'
import {upload, complete} from '@/api/upload'

export default {
  data() {
    return {
      keyframe_loading: false,
      checked: [false, false, false, false, false, false, false, false, false, false],
      active_keyframe: {
        id: null,
        keyframe_Description: null,
        keyframe_time: null,
        keyframe_Focus: 0,
        chapter: null,
        is_edit: false,
      },

      lessonBrief: {},
      chapterVideoList: [],
      is_video_update: false,
      edit_id: -1,
      dialogForm: {
        chapterTitle: null,
        chapterID: null,
        chapterFile: null,
        training: null,
        prevChapter: null,
        url: null
      },
      dialogChapterFormVisible: false, // 修改或添加章节表单
      // 四种课程类型
      dialogVideoVisible1: false,
      dialogVideoVisible2: false,
      dialogVideoVisible3: false,
      dialogVideoVisible4: false,
      dialogTitle: '', // 弹框标题
      fileList: [], // 上传文件列表
      videoChapterId: '',
      wait_pre_commit: false,
      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0], // 可选的播放速度
        autoplay: false, // 如果为true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 是否视频一结束就重新开始。
        preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [{
          type: 'video/mp4', // 类型
          src: '' // url地址
        }],
        poster: '', // 封面地址
        notSupportedMessage: '此视频暂无法播放，请稍后再试', // 允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true, // 当前时间和持续时间的分隔符
          durationDisplay: true, // 显示持续时间
          remainingTimeDisplay: false, // 是否显示剩余时间功能
          fullscreenToggle: true // 是否显示全屏按钮
        }
      },
      current: null,
      lessonType: 4,
      time: '',
      answerList: [],
      keyframeList: [],
      currentAnswer: {},
      actionList: [],
      action: null,
      emotion: null,
      mood: null,
      rules: {
        chapterTitle: [{required: true, message: '视频标题不能为空', trigger: 'blur'}],
        chapterID: [{required: true, message: '视频编码不能为空', trigger: 'blur'}],
        chapterFile: [{required: true, message: '视频文件不能为空', trigger: 'blur'}]
      },
      answerRules: {
        start_time: [{required: true, message: '开始时间不能为空', trigger: 'blur'}],
        end_time: [{required: true, message: '结束时间不能为空', trigger: 'blur'}],
        action: [{required: true, message: '参考动作不能为空', trigger: 'change'}]
      },
      fileMD5: '',
      progress: 0,
      progressVisible: false
    }
  },

  created() {
    this.getLessonDetail()
    this.getAction()
    this.getChapterVideo()
  },

  methods: {
    activeKeyframe(item) {
      this.active_keyframe.id = item.id
      this.active_keyframe.keyframe_Description = item.keyframe_Description
      this.active_keyframe.keyframe_time = item.keyframe_time
      this.skipTime(item.keyframe_time / 1000)
      // alert(this.current)
      this.active_keyframe.keyframe_Focus = item.keyframe_Focus
      this.active_keyframe.chapter = item.chapter
      this.active_keyframe.is_edit = true
      for (let base = 0; base < 10; base++) {
        // console.log(2 ** base)
        if ((item.keyframe_Focus & (2 ** base)) > 0) {
          this.checked[base] = true
        } else {
          this.checked[base] = false
        }
      }
    },
    resetKeyframe() {
      this.checked = [false, false, false, false, false, false, false, false, false, false]
    },
    submitKeyframe() {
      let focus = 0
      for (let base = 0; base < 10; base++) {

        if (this.checked[base] === true) {
          focus += (2 ** base)
        }
      }
      this.active_keyframe.keyframe_Focus = focus
      editChapterKeyframe(this.active_keyframe.id, {
        keyframe_Description: this.active_keyframe.keyframe_Description,
        keyframe_time: this.active_keyframe.keyframe_time,
        keyframe_Focus: this.active_keyframe.keyframe_Focus,
        chapter: this.active_keyframe.chapter
      }).then(() => {
        this.$message.success('提交成功')
      }).finally(
        () => {
          this.getKeyframe()
        }
      )
    },
    getKeyframe() {
      getChapterKeyframe({chapter_id: this.videoChapterId}).then(res => {
        this.keyframeList = res
      })
    },
    generateKeyframe() {
      if (this.keyframeList.length !== 0 || this.keyframe_loading) {
      } else {
        this.keyframe_loading = true
        generateChapterKeyframe({chapter_id: this.videoChapterId}).then(() => {
          this.$message.success('生成关键帧成功')
          this.keyframe_loading = false
        }).finally(() => {
          this.getKeyframe()
          this.keyframe_loading = false
        })
      }
    },
    getLessonDetail() {
      getOneTraining(this.$route.query.id).then(res => {
        this.lessonBrief = res
      })
    },
    getAction() {
      getActionList({no_page: 1}).then(res => {
        this.actionList = res
      })
    },
    getChapterVideo() {
      getChapterList({training_id: this.$route.query.id}).then(res => {
        this.chapterVideoList = res
      })
    },
    videoHttpRequest(option) {
      this.progressVisible = true
      this.is_video_update = true
      const file = option.file
      const isLt10M = file.size / 1024 / 1024 / 1024 < 2
      if (['video/mp4', 'video/ogg', 'video/flv', 'video/avi', 'video/wmv', 'video/rmvb'].indexOf(file.type) === -1) {
        this.$message.error('请上传正确的视频格式')
        this.handleVideoRemove()
        return
      }
      if (!isLt10M) {
        this.$message.error('上传视频大小不能超过2G哦!')
        this.handleVideoRemove()
        return
      }
      this.fileList.push(file)
      this.dialogForm.chapterFile = this.fileList[0]
      this.uploadByPieces({file: this.dialogForm.chapterFile, pieceSize: 50})
    },
    handleVideoRemove() {
      this.dialogForm.chapterFile = ''
      this.dialogForm.url = null
      this.progress = 0
      this.progressVisible = false
      this.fileList = []
      this.is_video_update = true
    },
    handleUploadExceed(files, fileList) {
      this.$message.warning('最多只能上传1个视频')
    },
    // 提交训练标准答案操作===========================================================
    editResult(id) {
      this.videoChapterId = id
      if (this.lessonType === 1) {
        this.dialogVideoVisible1 = true
        this.getAnswer()
      } else if (this.lessonType === 2) {
        this.dialogVideoVisible2 = true
        this.getAnswer()
      } else if (this.lessonType === 3) {
        this.dialogVideoVisible3 = true
        this.getAnswer()
      } else if (this.lessonType === 4) {
        this.dialogVideoVisible4 = true
        this.getKeyframe()
      }
      // 设置视频与封面
      getChapter(id).then(res => {
        this.playerOptions.sources[0].src = res.chapterFile
        this.playerOptions.poster = null
      })
    },
    getAnswer() {
      getChapterPoints({chapter_id: this.videoChapterId}).then(res => {
        this.answerList = res
      })
    },
    // 添加视频信息
    addResult() {
      // alert(this.videoChapterId)
      if (this.playerOptions.sources[0].src === '') {
        this.$message.error('没有视频，请先添加教学视频')
        return
      } else if (this.wait_pre_commit) {
        this.$message.error('请先添加上一个参考动作')
        return
      } else {
        if (this.current == null) {
          this.onPlayerPlay()
        }
        this.currentAnswer = {
          start_time: null,
          action: null,
          emotion: null,
          mood: null,
          end_time: null,
          chapter: this.videoChapterId,
          wait_commit: true
        }
        this.answerList.push(this.currentAnswer)
        this.wait_pre_commit = true
      }
    },
    setStartTime() {
      this.onPlayerPause()
      this.currentAnswer.start_time = parseInt(this.current * 1000)
    },
    setEndTime() {
      this.onPlayerPause()
      this.currentAnswer.end_time = parseInt(this.current * 1000)
      // console.log(this.actionList)
    },
    skipTime(time) {
      // 跳转到对应的时间
      this.$refs.videoPlayer.player.currentTime(time)
    },
    addAnswerList(answer) {
      if (answer.start_time === null || answer.end_time === null) {
        this.$message.error('请完整填写参考动作的开始时间、结束时间，选择动作信息')
        return
      }
      addChapterPoints(answer).then(() => {
        this.$message.success('参考动作添加成功')
      }).finally(() => {
        this.getAnswer()
        this.wait_pre_commit = false
      })
    },
    deleteAnswer(item) {
      this.$confirm('确定要删除吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteChapterPoints(item.id).then(() => {
          this.$message.success('删除成功')
        }).finally(() => {
          this.getAnswer()
        })
      })
    },


    // 监听播放
    onPlayerPlay(player) {
      // console.log('监听播放')
      this.$refs.videoPlayer.player.play()
    },
    // 监听暂停
    onPlayerPause(player) {
      // console.log('监听暂停')
      this.$refs.videoPlayer.player.pause()
    },
    // 监听媒体是否到达结尾，播放完
    onPlayerEnded(player) {
      // console.log(player)
    },
    // 当前播放位置发生变化时触发。
    onPlayerTimeupdate(player) {
      this.current = player.cache_.currentTime
    },
    // 章节操作============================================================
    // 删除章节
    removeChapter(chapterId) {
      this.$confirm('此操作将永久删除该视频, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteChapter(chapterId).then(res => {
          this.$message.success('删除成功')
        }).finally(() => {
          this.getChapterVideo()
        })
      })
    },
    // 修改章节按钮
    editChapter(chapterId) {
      this.dialogChapterFormVisible = true
      this.dialogTitle = '修改视频'
      this.edit_id = chapterId
      getChapter(chapterId).then(res => {
        this.dialogForm = res
        const ele = this.dialogForm.chapterFile
        if (ele) {
          const obj = {}
          const index = ele.lastIndexOf('\/')
          const fileName = ele.substring(index + 1, ele.length)
          obj['name'] = fileName
          obj['url'] = ele
          this.fileList.push(obj)
        }
      })
      this.is_video_update = false
    },
    openChapterDialog() {
      this.dialogChapterFormVisible = true
      this.dialogTitle = '添加视频'
    },
    handleAddChapter() {
      const params = new FormData()
      params.append('chapterTitle', this.dialogForm.chapterTitle)
      params.append('chapterID', this.dialogForm.chapterID)
      params.append('training', this.$route.query.id)
      params.append('url', this.dialogForm.url)
      addChapter(params).then(res => {
        this.$message.success('添加视频成功')
      }).finally(() => {
        this.getChapterVideo()
        this.handleCancel()
      })
    },
    handleUpdateChapter() {
      const params = new FormData()
      params.append('chapterTitle', this.dialogForm.chapterTitle)
      params.append('chapterID', this.dialogForm.chapterID)
      params.append('training', this.$route.query.id)
      if (this.is_video_update) {
        params.append('url', this.dialogForm.url)
      }
      updateChapter(this.dialogForm.id, params).then(res => {
        this.$message.success('修改视频成功')
      }).finally(() => {
        this.getChapterVideo()
        this.handleCancel()
      })
    },
    uploadByPieces({file, pieceSize}) {
      const chunkSize = pieceSize * 1024 * 1024 // 50MB一片
      const chunkCount = Math.ceil(file.size / chunkSize) // 总片数
      const fileReaderInstance = new FileReader()
      fileReaderInstance.readAsBinaryString(file)
      fileReaderInstance.addEventListener('load', e => {
        const fileBolb = e.target.result
        this.fileMD5 = md5(fileBolb)
        this.sequentialUplode(file, 0, chunkSize, chunkCount)
      })
    },
    sequentialUplode(file, currentChunk, chunkSize, chunkCount) {
      const {chunk} = this.getChunkInfo(file, currentChunk, chunkSize)
      const chunkInfo = {chunk, currentChunk, chunkCount}
      // console.log('当前上传分片：' + currentChunk)
      const fetchForm = new FormData()
      fetchForm.append('chunkNumber', chunkInfo.currentChunk)
      fetchForm.append('file', chunkInfo.chunk)
      fetchForm.append('identifier', this.fileMD5)
      // 执行分片上传
      upload(fetchForm).then(res => {
        if (res.code === 0) {
          // 判断是否全部上传完
          if (chunkInfo.currentChunk === chunkInfo.chunkCount) {
            complete({'identifier': this.fileMD5, 'file_name': file.name}).then(res => {
              this.dialogForm.url = res.url
              this.$message.success('视频上传成功！')
              this.progress = 100
            }).catch((e) => {
              this.$message.error('视频上传失败！请删除该视频重新上传')
            })
          } else {
            this.progress = parseInt(currentChunk / chunkCount * 100)
            this.sequentialUplode(file, currentChunk + 1, chunkSize, chunkCount)
          }
        }
      }).catch((e) => {
        this.$message.error(e)
      })
    },
    getChunkInfo(file, currentChunk, chunkSize) {
      const start = currentChunk * chunkSize
      const end = Math.min(file.size, start + chunkSize)
      const chunk = file.slice(start, end)
      return {start, end, chunk}
    },
    handleConfirm() {
      this.$refs['dialogForm'].validate(valid => {
        if (!valid) {
          this.$message.error('请检查必填项是否填写正确！')
          return
        } else if (this.dialogForm.url === null || this.dialogForm.url === '') {
          this.$message.error('请等待视频上传')
        } else {
          // this.uploadByPieces({ file: this.video, pieceSize: 100 })
          if (this.dialogTitle === '添加视频') {
            this.handleAddChapter()
          } else if (this.dialogTitle === '修改视频') {
            this.handleUpdateChapter()
          }
          this.handleCancel()
          setTimeout(() => {
            this.getChapterVideo()
          }, 100)
        }
      })
    },
    handleCancel() {
      this.dialogChapterFormVisible = false
      this.$refs.dialogForm.resetFields()
      this.fileMD5 = ''
      this.progress = 0
      this.dialogForm.url = null
      this.fileList = []
      this.progressVisible = false
    },
    closeVideoDialog() {
      if (this.lessonType === 1) {
        this.dialogVideoVisible1 = false
      } else if (this.lessonType === 2) {
        this.dialogVideoVisible2 = false
      } else if (this.lessonType === 3) {
        this.dialogVideoVisible3 = false
      } else if (this.lessonType === 4) {
        this.dialogVideoVisible4 = false
        this.active_keyframe = {
          id: null,
          keyframe_Description: null,
          keyframe_time: null,
          keyframe_Focus: 0,
          chapter: null
        }
        this.checked = [false, false, false, false, false, false, false, false, false, false]
      }
      this.answerList = []
      this.keyframeList = []
      this.wait_pre_commit = false
    },
    // 发布课程按钮
    publish() {
      this.$confirm('确定要发布该课程吗？发布后无法修改！', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        doPublish({training_id: this.$route.query.id}).then(() => {
          this.$message.success('发布课程成功')
        }).finally(() => {
          this.$router.replace({path: 'lessonList'})
        })
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.active {
  background: rgba(255, 241, 242, 1) !important;
  border: 1px solid rgba(235, 70, 84, 1);
}

.el-header, .el-footer {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 35px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;

  line-height: 100px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.course-label {
  min-height: 200px;
  padding: 20px;
  border-radius: 4px;
  margin: -10px;
  display: flex;
}

.leftImg {
  width: 300px;
  height: 200px;
  margin: 20px;

  .imgStyle {
    width: 300px;
    height: 200px;
    object-fit: cover;
    display: block;
    border-radius: 4px;
    position: relative;
  }
}

.rightCon {
  padding: 20px;
  margin: 10px;
}

.title {
  margin-top: 8px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.teacher {
  padding: 12px 0;
  color: #999;
  font-size: 12px;
}

.info {
  font-size: 14px;
  color: #999;
  line-height: 22px;
  height: 66px;
  overflow: hidden;
  position: relative;
}

.chapterList {
  position: relative;
  list-style: none;
  margin: 0;
  padding: 0;
}

.chapterList li {
  position: relative;
}

.chapterList p {
  float: left;
  font-size: 20px;
  margin: 10px 0;
  padding: 10px;
  height: 70px;
  line-height: 50px;
  width: 100%;
  border: 1px solid #DDD;
}

.chapterList .acts {
  float: right;
  font-size: 14px;
}

.answer-list {
  list-style: none;
}

</style>
