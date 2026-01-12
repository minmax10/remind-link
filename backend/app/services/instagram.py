"""
인스타그램 연동 서비스
instagrapi를 사용하여 인스타그램 저장글 가져오기
"""
from typing import List, Dict, Optional
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired
import logging

logger = logging.getLogger(__name__)


class InstagramService:
    """인스타그램 연동 서비스"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.client = Client()
        self.authenticated = False
    
    def login(self) -> bool:
        """인스타그램 로그인"""
        try:
            self.client.login(self.username, self.password)
            self.authenticated = True
            logger.info(f"인스타그램 로그인 성공: {self.username}")
            return True
        except TwoFactorRequired:
            logger.error("2단계 인증이 필요합니다")
            raise Exception("2단계 인증이 필요합니다. 앱 비밀번호를 사용하세요")
        except Exception as e:
            logger.error(f"인스타그램 로그인 실패: {str(e)}")
            raise Exception(f"로그인 실패: {str(e)}")
    
    def get_saved_posts(self, limit: int = 50) -> List[Dict]:
        """
        저장된 게시물 가져오기
        
        Args:
            limit: 가져올 게시물 수
            
        Returns:
            저장된 게시물 리스트
        """
        if not self.authenticated:
            raise Exception("인스타그램에 로그인되지 않았습니다")
        
        try:
            saved_posts = []
            
            # 사용자 ID 가져오기
            user_id = self.client.user_id_from_username(self.username)
            
            try:
                # 방법 1: 컬렉션을 통한 저장된 게시물 가져오기
                try:
                    collections = self.client.collections()
                    logger.info(f"컬렉션 개수: {len(collections)}")
                    
                    for collection in collections:
                        try:
                            # 컬렉션 ID 가져오기
                            collection_id = collection.collection_id if hasattr(collection, 'collection_id') else collection.get('collection_id')
                            if not collection_id:
                                continue
                            
                            # 컬렉션의 미디어 가져오기
                            collection_medias = self.client.collection_medias(
                                collection_id=collection_id,
                                amount=limit
                            )
                            
                            for media in collection_medias:
                                post_data = self._format_post(media)
                                if post_data:
                                    saved_posts.append(post_data)
                                    
                            if len(saved_posts) >= limit:
                                break
                                
                        except Exception as e:
                            logger.warning(f"컬렉션 미디어 가져오기 실패: {str(e)}")
                            continue
                    
                    if saved_posts:
                        # 중복 제거
                        seen_ids = set()
                        unique_posts = []
                        for post in saved_posts:
                            if post['id'] not in seen_ids:
                                seen_ids.add(post['id'])
                                unique_posts.append(post)
                        
                        return unique_posts[:limit]
                    
                except Exception as e:
                    logger.warning(f"컬렉션 방법 실패: {str(e)}")
                
                # 방법 2: 사용자 미디어에서 최근 게시물 가져오기 (대안)
                logger.info("최근 미디어를 대안으로 사용")
                return self._get_recent_media_as_fallback(limit)
                
            except Exception as e:
                logger.error(f"저장된 게시물 가져오기 실패: {str(e)}")
                raise
                
        except LoginRequired:
            logger.error("로그인이 필요합니다")
            raise Exception("인스타그램 세션이 만료되었습니다. 다시 로그인해주세요")
        except Exception as e:
            logger.error(f"저장된 게시물 가져오기 오류: {str(e)}")
            raise Exception(f"저장된 게시물을 가져오는데 실패했습니다: {str(e)}")
    
    def _format_post(self, media) -> Optional[Dict]:
        """미디어 객체를 표준 형식으로 변환"""
        try:
            # instagrapi의 Media 객체 처리
            if hasattr(media, 'dict'):
                media_dict = media.dict()
            elif hasattr(media, '__dict__'):
                media_dict = media.__dict__
            else:
                media_dict = media
            
            # URL 생성
            post_id = media_dict.get('id') or media_dict.get('pk') or media_dict.get('media_id')
            if not post_id:
                return None
            
            code = media_dict.get('code') or media_dict.get('shortcode', '')
            url = f"https://www.instagram.com/p/{code}/" if code else f"https://www.instagram.com/p/{post_id}/"
            
            # 이미지 URL 추출
            image_url = None
            if hasattr(media, 'thumbnail_url'):
                image_url = media.thumbnail_url
            elif media_dict.get('thumbnail_url'):
                image_url = media_dict['thumbnail_url']
            elif hasattr(media, 'photo_url'):
                image_url = media.photo_url
            elif media_dict.get('photo_url'):
                image_url = media_dict['photo_url']
            elif hasattr(media, 'image_url'):
                image_url = media.image_url
            elif media_dict.get('image_url'):
                image_url = media_dict['image_url']
            elif hasattr(media, 'thumbnail_resources') and media.thumbnail_resources:
                # 썸네일 리소스에서 가장 큰 이미지 선택
                image_url = media.thumbnail_resources[-1].get('src') if isinstance(media.thumbnail_resources[-1], dict) else media.thumbnail_resources[-1].src
            
            # 캡션 추출
            caption_text = ''
            if hasattr(media, 'caption_text'):
                caption_text = media.caption_text or ''
            elif hasattr(media, 'caption'):
                caption = media.caption
                if isinstance(caption, dict):
                    caption_text = caption.get('text', '')
                else:
                    caption_text = str(caption) if caption else ''
            elif media_dict.get('caption_text'):
                caption_text = media_dict['caption_text']
            elif media_dict.get('caption'):
                caption = media_dict['caption']
                if isinstance(caption, dict):
                    caption_text = caption.get('text', '')
                else:
                    caption_text = str(caption) if caption else ''
            
            return {
                'id': str(post_id),
                'url': url,
                'title': caption_text[:100] if caption_text else '인스타그램 게시물',
                'description': caption_text,
                'image_url': image_url,
                'source': 'instagram',
                'metadata': {
                    'instagram': {
                        'post_id': str(post_id),
                        'code': code,
                        'like_count': getattr(media, 'like_count', media_dict.get('like_count', 0)),
                        'comment_count': getattr(media, 'comment_count', media_dict.get('comment_count', 0)),
                        'taken_at': getattr(media, 'taken_at', media_dict.get('taken_at')),
                    }
                }
            }
        except Exception as e:
            logger.error(f"포스트 포맷팅 실패: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _get_recent_media_as_fallback(self, limit: int) -> List[Dict]:
        """대안: 최근 미디어 가져오기 (저장된 게시물이 아닐 수 있음)"""
        try:
            user_id = self.client.user_id_from_username(self.username)
            medias = self.client.user_medias(user_id, amount=limit)
            
            posts = []
            for media in medias:
                post_data = self._format_post(media)
                if post_data:
                    posts.append(post_data)
            
            logger.info(f"최근 미디어 {len(posts)}개 가져옴")
            return posts
        except Exception as e:
            logger.error(f"최근 미디어 가져오기 실패: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
