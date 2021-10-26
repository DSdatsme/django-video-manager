
import logging

# django dependencies
from rest_framework.views import APIView
from rest_framework.response import Response

# project dependencies
from . import helpers
from .models import Video, get_video_by_id

from video_manager.constants import DEFAULT_VIDEO_FOLDER

logger = logging.getLogger('django')


class VideoAlreadyExistsException(Exception):
    pass


class VideosApi(APIView):

    def get(self, _):
        response = {
            "message": {},
            "status_code": 200
        }
        try:
            complete_video_list = []
            for each_video in Video.objects.all():
                complete_video_list.append(
                    helpers.get_video_metadata_response(each_video)
                )
            response["message"] = {"videos": complete_video_list}
            logger.info(f"Videos found {len(complete_video_list)}")
        except Exception as err:
            logger.error(err)
            response["message"] = "Fetching Video list failed"
            response['status_code'] = 500
        return Response(response['message'], status=response['status_code'], headers=None)

    def post(self, request):
        response = {
            "message": {},
            "status_code": 201
        }
        try:
            file_name = helpers.get_field_value('video_name', request)
            video_folder = helpers.get_field_value('video_folder', request)

            if helpers.video_exists(video_folder + file_name):
                raise VideoAlreadyExistsException

            file_path = helpers.save_video_file(
                video_folder + file_name, request.data.get('video_file'))
            video_metadata = helpers.get_video_data(
                DEFAULT_VIDEO_FOLDER + file_path)

            new_video = Video(name=file_name,
                              size=video_metadata['format']['size'],
                              path=video_folder,
                              duration=video_metadata['format']['duration'],
                              codec=video_metadata['format']['format_name'],
                              container=video_metadata['format']['tags']['major_brand'])
            new_video.save()
            response["message"] = helpers.get_video_metadata_response(
                new_video)
            logger.info(f"video upload successfully with id {new_video.id}")
        except VideoAlreadyExistsException as err:
            logger.error(err)
            response["message"] = f"Video with the name {file_name} already present at that path {video_folder}."
            logger.error(response["message"])
            response['status_code'] = 409
        except Exception as err:
            logger.error(err)
            try:
                # delete video if it was present
                helpers.delete_video_file(file_path)
                logger.info("video deleted")
            except:
                logger.info("video was not saved")
            response["message"] = "Video Upload failed, please try again"
            response['status_code'] = 500

        return Response(response['message'], status=response['status_code'], headers=None)


class VideoMetadataApi(APIView):
    def get(self, _, video_id):
        response = {
            "message": {},
            "status_code": 200
        }
        try:
            required_video = get_video_by_id(video_id)
            response["message"] = helpers.get_video_metadata_response(
                required_video)
            logger.info(f"video found with ID {required_video.id}")
        except Exception as err:
            logger.error(err)
            response["message"] = f"Video with ID {video_id} not found in system"
            response['status_code'] = 404

        return Response(response['message'], status=response['status_code'], headers=None)

    def put(self, request, video_id):
        response = {
            "message": {},
            "status_code": 200
        }
        try:
            required_video = get_video_by_id(video_id)
            current_path = required_video.path + required_video.name
            updated_fields = request.data

            for each_field_name, each_field_value in updated_fields.items():
                if each_field_name == "video_name":
                    required_video.name = each_field_value
                elif each_field_name == "video_folder":
                    required_video.path = each_field_value

            if current_path != required_video.path + required_video.name:       # move file if change in name/folder
                logger.info("path not same")
                logger.debug(
                    f"Current Path: {current_path}, new path: {required_video.path + required_video.name}")

                helpers.move_file(DEFAULT_VIDEO_FOLDER + current_path,
                                  DEFAULT_VIDEO_FOLDER + required_video.path + required_video.name)
                logger.info(f"file moved to destination {DEFAULT_VIDEO_FOLDER + required_video.path + required_video.name} for video id {video_id}")
            required_video.save()       # save entry in db
            response["message"] = helpers.get_video_metadata_response(
                required_video)
        except Exception as err:
            logger.error(err)
            response["message"] = "Error occured while updating video metadata"
            response['status_code'] = 500
        return Response(response['message'], status=response['status_code'], headers=None)

    def delete(self, _, video_id):

        response = {
            "message": {},
            "status_code": 200
        }
        try:
            required_video = get_video_by_id(video_id)
            response["message"] = helpers.get_video_metadata_response(
                required_video)

            file_path = helpers.delete_video_file(
                required_video.path + required_video.name)  # delete video from filesystem
            
            required_video.delete()
            logger.error(f"Video deleted with ID {video_id}")
        except Exception as err:
            logger.error(err)
            response["message"] = f"Video with ID {video_id} not found"
            logger.error(response["message"])
            response['status_code'] = 404
        return Response(response['message'], status=response['status_code'], headers=None)
