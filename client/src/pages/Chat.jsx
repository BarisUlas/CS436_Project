import  { useState, useMemo, useRef } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import Model from '../components/Model'
import { BsEmojiSmile, BsFillEmojiSmileFill } from 'react-icons/bs'
import { MdKeyboardVoice } from "react-icons/md";
import { fetchMessages, sendMessage } from '../apis/messages'
import { useEffect } from 'react'
import MessageHistory from '../components/MessageHistory'
import io from 'socket.io-client'
import './home.css'
import { fetchChats, setNotifications } from '../redux/chatsSlice'
import Loading from '../components/ui/Loading'
import data from '@emoji-mart/data'
import Picker from '@emoji-mart/react'
import { getChatName } from '../utils/logics'
import Typing from '../components/ui/Typing'
import { validUser } from '../apis/auth'
let socket, selectedChatCompare

function Chat(props) {
  const { activeChat, notifications } = useSelector((state) => state.chats)
  const dispatch = useDispatch()
  const [event, setEvent] = useState(null);
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [socketConnected, setSocketConnected] = useState(false)
  const [typing, setTyping] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const [loading, setLoading] = useState(false)
  const [showPicker, setShowPicker] = useState(false)
  const activeUser = useSelector((state) => state.activeUser)
  const isChatBot = useMemo(() => {
    return activeChat?.users?.length && activeChat?.users[0].name === "Chat Bot";
  });

  const inputFile = useRef(null);
  const voiceFile = useRef(null);

  const keyDownFunction = async (e) => {
    if ((e.key === 'Enter' || e.type === 'click') && message) {
      setMessage('')
      socket.emit('stop typing', activeChat._id)
      const data = await sendMessage({ chatId: activeChat._id, message })
      console.log(data)
      socket.emit('new message', data)
      setMessages([...messages, data])
      dispatch(fetchChats())
    }
  }

  useEffect(() => {
    socket = io('')
    socket.on('typing', () => setIsTyping(true))
    socket.on('stop typing', () => setIsTyping(false))
  }, [])

  useEffect(() => {
    socket.emit('setup', activeUser)
    socket.on('connected', () => {
      setSocketConnected(true)
    })
  }, [messages, activeUser])
  useEffect(() => {
    const fetchMessagesFunc = async () => {
      if (activeChat) {
        setLoading(true)
        const data = await fetchMessages(activeChat._id)
        setMessages(data)
        socket.emit('join room', activeChat._id)
        setLoading(false)
      }
      return
    }
    fetchMessagesFunc()
    selectedChatCompare = activeChat
  }, [activeChat])
  useEffect(() => {
    socket.on('message recieved', (newMessageRecieved) => {
      if (
        (!selectedChatCompare || selectedChatCompare._id) !==
        newMessageRecieved.chatId._id
      ) {
        if (!notifications.includes(newMessageRecieved)) {
          dispatch(setNotifications([newMessageRecieved, ...notifications]))
        }
      } else {
        setMessages([...messages, newMessageRecieved])
      }
      dispatch(fetchChats())
    })
  })
  useEffect(() => {
    const isValid = async () => {
      const data = await validUser()
      if (!data?.user) {
        window.location.href = '/login'
      }
    }
    isValid()
  }, [])
  if (loading) {
    return (
      <div className={props.className}>
        <Loading />
      </div>
    )
  }

  const onBlurButtonClick = () => {
    setEvent("blurring");
    inputFile.current.click();
  };

  const onBWButtonClick = () => {
    setEvent("bw")
    inputFile.current.click();
  };

  const onHelpButtonClick = async () => {
    const data = await sendMessage({ chatId: activeChat._id, message: JSON.stringify({action: "help"}) }) 
    setMessages([...messages, ...data]);
  }


  const handleVoiceButtonClick = () => {
    voiceFile.current.click();
  }

  const handleFile = async (e) => {
    const file = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async function () {
      const data = await sendMessage({ chatId: activeChat._id, message: JSON.stringify({action: event, image: reader.result}) }) 
      setMessages([...messages, ...data]);
    };
    reader.onerror = function (error) {
        console.log('Error: ', error);
    };
  }
  
  const handleVoice = async (e) => {
    const file = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async function () {
      const data = await sendMessage({ type: "audio", chatId: activeChat._id, message: reader.result }) 
      setMessages([...messages, data]);
    };
    reader.onerror = function (error) {
        console.log('Error: ', error);
    };
    
  };


  return (
    <>
    <input type='file' id='file' ref={inputFile} style={{display: 'none'}} onChange={handleFile} accept=".png" />
    <input type='file' id='voice' ref={voiceFile} style={{display: 'none'}} onChange={handleVoice} accept='.mp3' />
      {activeChat ? (
        <div className={props.className}>
          <div className="flex justify-between items-center px-5 bg-[#ffff] w-[100%]">
            <div className="flex items-center gap-x-[10px]">
              <div className="flex flex-col items-start justify-center">
                <h5 className="text-[17px] text-[#2b2e33] font-bold tracking-wide">
                  {getChatName(activeChat, activeUser)}
                </h5>
                {/* <p className='text-[11px] text-[#aabac8]'>Last seen 5 min ago</p> */}
              </div>
            </div>
            <div>
              <Model />
            </div>
          </div>
          <div className="scrollbar-hide w-[100%] h-[70vh] md:h-[66vh] lg:h-[69vh] flex flex-col overflow-y-scroll p-4">
            <MessageHistory typing={isTyping} messages={messages} />
            <div className="ml-7 -mb-10">
              {isTyping ? <Typing width="100" height="100" /> : ''}
            </div>
          </div>
          <div className="absolute left-[31%] bottom-[8%]">{
            isChatBot ? (
              <div className="space-x-2">
                <button
                  onClick={onHelpButtonClick}
                  className="bg-[#f8f9fa] border-[2px] border-[#d4d4d4] text-[14px] px-2 py-[3px] text-[#9e9e9e] font-medium rounded-[7px] -mt-1"
                >
                  Help
                </button>
                <button
                  onClick={onBWButtonClick}
                  className="bg-[#f8f9fa] border-[2px] border-[#d4d4d4] text-[14px] px-2 py-[3px] text-[#9e9e9e] font-medium rounded-[7px] -mt-1"
                >
                  Black and White
                </button>
                <button
                  onClick={onBlurButtonClick}
                  className="bg-[#f8f9fa] border-[2px] border-[#d4d4d4] text-[14px] px-2 py-[3px] text-[#9e9e9e] font-medium rounded-[7px] -mt-1"
                >
                  Blur
                </button> 
              </div>
            ) : 
            (
              <>
            {showPicker && (
              <Picker
                data={data}
                onEmojiSelect={(e) => setMessage(message + e.native)}
              />
            )}
            <div className="border-[1px] border-[#aabac8] px-6 py-3 w-[360px] sm:w-[400px] md:w-[350px] h-[50px] lg:w-[400px] rounded-t-[10px]">
              <form
                onKeyDown={(e) => keyDownFunction(e)}
                onSubmit={(e) => e.preventDefault()}
              >
                <input
                  onChange={(e) => {
                    setMessage(e.target.value)
                    if (!socketConnected) return
                    if (!typing) {
                      setTyping(true)
                      socket.emit('typing', activeChat._id)
                    }
                    let lastTime = new Date().getTime()
                    var time = 3000
                    setTimeout(() => {
                      var timeNow = new Date().getTime()
                      var timeDiff = timeNow - lastTime
                      if (timeDiff >= time && typing) {
                        socket.emit('stop typing', activeChat._id)
                        setTyping(false)
                      }
                    }, time)
                  }}
                  className="focus:outline-0 w-[100%] bg-[#f8f9fa]"
                  type="text"
                  name="message"
                  placeholder="Enter message"
                  value={message}
                />
              </form>
            </div>

            <div className="border-x-[1px] border-b-[1px] bg-[#f8f9fa] border-[#aabac8] px-6 pl-3 py-3 w-[360px] sm:w-[400px] md:w-[350px] lg:w-[400px] rounded-b-[10px] h-[50px]">
              {/* {
                  isTyping ? <div>Loading</div> : ""
                } */}
              <div className="flex justify-between items-start">
                <div className='flex'>
                  <div className='cursor-pointer' onClick={handleVoiceButtonClick}>
                    <MdKeyboardVoice className='w-[20px] h-[20px] border-[black] mr-2' />
                  </div>
                  <div
                    className="cursor-pointer"
                    onClick={() => setShowPicker(!showPicker)}
                  >
                    {showPicker ? (
                      <BsFillEmojiSmileFill className="w-[20px] h-[20px] text-[#ffb02e] border-[black]" />
                    ) : (
                      <BsEmojiSmile className="w-[20px] h-[20px]" />
                    )}
                  </div>
                </div>
                <button
                  onClick={(e) => keyDownFunction(e)}
                  className="bg-[#f8f9fa] border-[2px] border-[#d4d4d4] text-[14px] px-2 py-[3px] text-[#9e9e9e] font-medium rounded-[7px] -mt-1"
                >
                  Send
                </button>
              </div>
            </div>
          </>
            )
          }</div>
        </div>
      ) : (
        <div className={props.className}>
          <div className="relative">
            <div className="absolute top-[40vh] left-[44%] flex flex-col items-center justify-center gap-y-3">
              <img
                className="w-[50px] h-[50px] rounded-[25px]"
                alt="User profile"
                src={activeUser.profilePic}
              />
              <h3 className="text-[#111b21] text-[20px] font-medium tracking-wider">
                Welcome{' '}
                <span className="text-[#166e48] text-[19px] font-bold">
                  {' '}
                  {activeUser.name}
                </span>
              </h3>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default Chat
