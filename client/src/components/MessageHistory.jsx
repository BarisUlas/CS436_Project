import React from 'react'
import { useSelector } from 'react-redux'
import ScrollableFeed from "react-scrollable-feed"
import { isSameSender, isSameSenderMargin, isSameUser, isLastMessage } from '../utils/logics'
import { Tooltip } from "@chakra-ui/tooltip";
import { Avatar } from "@chakra-ui/avatar";
import ReactPlayer from 'react-player'

import "../pages/home.css"
function MessageHistory({ messages }) {
  const activeUser = useSelector((state) => state.activeUser)

  return (
    <>
      <ScrollableFeed className='scrollbar-hide'>
        {messages &&
          messages.map((m, i) => (

            <div className='flex items-center gap-x-[6px]' key={m._id} >
              {(isSameSender(messages, m, i, activeUser.id) ||
                isLastMessage(messages, i, activeUser.id)) && (
                  <Tooltip label={m.sender?.name} placement="bottom-start" hasArrow>
                    <Avatar
                      style={{ width: "32px", height: "32px" }}
                      mt="43px"
                      mr={1}

                      cursor="pointer"
                      name={m.sender?.name}
                      src={m.sender?.profilePic}
                      borderRadius="25px"
                    />
                  </Tooltip>

                )}
              <span className='tracking-wider text-[15px]  font-medium'
                style={{
                  backgroundColor: `${m.sender._id === activeUser.id ? "#268d61" : "#f0f0f0"
                    }`,
                  marginLeft: isSameSenderMargin(messages, m, i, activeUser.id),
                  marginTop: isSameUser(messages, m, i, activeUser.id) ? 3 : 10,
                  borderRadius: `${m.sender._id === activeUser.id ? "10px 10px 0px 10px" : "10px 10px 10px 0"}`,
                  padding: "10px 18px",
                  maxWidth: "460px",
                  color: `${m.sender._id === activeUser.id ? "#ffff" : "#848587"}`
                }}
              >
                {
                  m.type === "audio" ? (
                    <div>
                      <audio controls className='bg-transparent' style={{backgroundColor: "transparent"}}>
  <source src={JSON.parse(m.message).url} type="audio/mp3" style={{backgroundColor: "transparent"}} />
</audio>
<div>{JSON.parse(m.message).transcription}</div>
                    </div>
                  ) : m.message.startsWith("https://") ? (
                   <img src={m.message} width={300} height={300} /> 
                  ) : (<div>{m.message}</div>)
                }
              </span>
            </div>
          ))
        }

      </ScrollableFeed >
    </>
  )
}

export default MessageHistory