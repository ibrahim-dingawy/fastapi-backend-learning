"""def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False"""
from app.models.video import Video

"""def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        needed = target - num

        if needed in seen:
            return [seen[needed], i]

        seen[num] = i

    return []"""

"""def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        needed = target - num
        if needed in seen:
            return [seen[needed], i]
        seen[num] = i
    return []
"""


"""
def has_pair_with_sum(nums, target):
    for 

"""



#nums = [3, 4, 6, 8]
#target = 10
"""def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        needed = target - num
        if
"""




"""ابدأ بمؤشر على أول رقم ومؤشر على آخر رقم.
طول ما الاتنين ماعدوش بعض، اجمع الرقمين.
لو المجموع هو الـtarget رجّع True.
لو المجموع أقل، حرّك left يمين عشان تجيب رقم أكبر.
لو المجموع أكبر، حرّك right شمال عشان تجيب رقم أصغر.
لو خلصنا وملاقيناش، رجّع False."""

"""left = 0
right = len(nums) - 1
nums = [1, 2, 3, 4, 6]
target = 6"""

"""def is_palindrome(word):
    left = 0
    right = len(word) - 1

    while left < right:
        if word[left] != word[right]:
            return  False
        left +=1
        right -= 1
    return True
"""

"""def is_palindrome(word):
    left = 0
    right = len(word) - 1

    while left < right:
        if left != right:
            return False

        left += 1
        right -= 1

    return True"""

"""def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if mid == target:
            return mid
        elif nums[mid] < target:
            mid += 1
        else:
            mid -= 1
    return -1"""

"""
def valid_parentheses(s):
    stack = []

    for char in s:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0"""



"""def valid_parentheses(s):
    stack = []

    pairs = {
        ")": "(",
        "]": "[",
        "}": "{"
    }

    for char in s:
        if char in "([{":
            stack.append(char)

        elif char in ")]}":
            if stack:
                if pairs[char] == stack[-1]:
                    stack.pop()
"""

"""
def is_anagram(s, t):
    counts = {}

    for char in s:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1

    for item in t:
        if item not in counts:
            return False

        counts[item] -= 1

        if len(counts) < 0:
            return False
    return all()"""

"""def most_frequent(nums):
    counts = {}

    for num in nums:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1

        big_num = None
        max_count = 0

        for number, count in counts.items():
            if count > max_count:
                max_count = count
                big_num = num

        return f"biggest number is {big_num}"""



"""def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        elif nums[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return -1
"""



"""def valid_parentheses(s):
    stack = []

    pairs = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    for char in s:
        if char in ")]}":
            stack.append(char)
        elif char in ")]}":
            
"""

"""
def max_sum_subarray(nums, k):
        window_sum = sum(nums[:k])
        max_sum = window_sum

        for right in range(k, len(nums)):
NOT FINISHED YET
"""


"""def print_list(head):
    current = head
    while current is not None:
        print(current.value)
    return current.next"""

"""videos = [
    {"id": 1, "title": "Python Basics", "status": "ready"},
    {"id": 2, "title": "FastAPI Tutorial", "status": "processing"},
    {"id": 3, "title": "Advanced Python", "status": "ready"},
]

def filter_videos(videos, keyword, status):
    results = []
    for video in videos:
        match_keyword = keyword is None or keyword in video["title"]
        match_status = status is None or status == video["status"]

        if match_keyword and match_status:
            results.append(video)
    return results"""






"""
video = {
    "id": 1,
    "title": "Python Basics",
    "status": "processing"
}

def mark_video_ready(video):
    if video["status"] == "processing":
        video["status"] = "ready"
        return video
    elif video["status"] == "ready":
        return video
    else:
        return "Invalid status transition"


def update_status(video, new_status):
    if video["status"] == "processing" and new_status in ["ready", "failed"]:
        video["status"] = new_status
        return video

    elif video["status"] == "failed" and new_status == "processing":
        video["status"] = new_status
        return video

    else:
        return "Invalid status transition"""

"""
videos = [
    "video1",
    "video2",
    "video3",
    "video4",
    "video5",
    "video6"
]
def paginate(videos, page, page_size):
    if page <= 0 or page_size <= 0:
        return "Invalid Values"

    start = (page - 1) * page_size
    end = start + page_size

    return videos[start:end]"""

"""nums = [4, 2, 7, 2, 9, 4]
def first_repeated(nums):
    new_nums = []
    for num in nums:
        if new_nums is not None:
            new_nums.append(num)
            if num in new_nums:
                return num
            else:
                return None
        """

"""
nums = [4, 5, 4, 6, 5, 7]
def first_unique(nums):
    counts = {}
    for num in nums:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1

    for num in counts:
        if counts[num] == 1:
            return num"""


"""nums = [0, 1, 0, 3, 12]

def move_zeros(nums):
    left = 0

    for right in range(len(nums)):
        if nums[right] != 0:
            nums[left] = nums[right]
            left += 1

    while left < len(nums):
        nums[left] = 0
        left += 1

    return nums
"""


"""nums = [1, 2, 3, 4, 5]
target = 6

def count_pairs(nums, target):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                count += 1
    return count"""




"""def count_pairs(nums, target):
    seen = set()
    count = 0

    for num in nums:
        needed = target - num
        if needed in seen:
            count += 1
            seen.add(num)"""


"""videos = [
    {"id": 1, "status": "ready"},
    {"id": 2, "status": "processing"},
    {"id": 3, "status": "ready"},
    {"id": 4, "status": "failed"},
    {"id": 5, "status": "ready"},
]


def most_frequent_status(videos):
    counts = {}

    for video in videos:
        status = video["status"]

        if status in counts:
            counts[status] += 1
        else:
            counts[status] = 1

    most_status = None
    max_count = 0

    for status, count in counts.items():
        if count > max_count:
            max_count = count
            most_status = status
    return most_status
"""


videos = [
        {"id": 1, "title": "Python Basics", "status": "ready"},
        {"id": 2, "title": "FastAPI Tutorial", "status": "processing"},
        {"id": 3, "title": "SQLAlchemy Basics", "status": "ready"},
    ]

def update_video_title(videos, video_id, new_title):
    for video in videos:
        if video["id"] == video_id:
            video["title"] = new_title
            return video
    return None

def update_video_status(videos, video_id, new_status):
    for video in videos:
        if video["id"] == video_id and new_status in ["processing", "ready", "failed"]:
            video["status"] = new_status
            return video
    return None



def create_video(videos, title, status):
    if title is None:
        return "Title is required"
    elif status not in ["processing", "ready", "failed"]:
        return "Invalid status"
    else:
        new_id = videos[-1]["id"] + 1
        new_video = {"id": new_id, "title": title, "status": status}
        videos.append(new_video)
        return new_video


def get_next_video_id(videos):
    if not videos:
        return 1
    new_id = videos[-1]["id"] + 1
    return new_id


def can_delete_video(video):
    for video in videos:
        if video["status"] == "processing":
            return False
    return True

def delete_video(videos, video_id):
    for video in videos:
        if video["id"] != video_id:
            return None
        if not can_delete_video(videos):
            return "Cannot delete processing video"
        videos.pop(video)
    return True






"""        if video["id"] == video_id and can_delete_video(videos):
            videos.pop(video)
            return True
"""




"""from sqlalchemy import select




def filter_videos(db, status=None, title=None):
    stmt = select(Video)
    if status is not None:
        stmt = stmt.where(Video.status == status)
    if title is not None:
        stmt = stmt.where(Video.title == title)
    vids = db.scalars(stmt).all()
    return vids"""


from sqlalchemy import select
"""
def update_video_title(db, video_id, new_title):
    video = db.get(Video, video_id)
    if not video:
        return None
    video.title = new_title
    db.commit()
    db.refresh(video)
    return video
"""

"""def delete_video(db, video_id):
    video = db.get(Video, video_id)
    if not video:
        return None
    db.delete(video)
    db.commit()
    db.refresh(video)
    return True


"""

def create_video(db, title, status):
    video = Video(
        title=title,
        status=status
    )

    if not title:
        return "title is required"
    if status not in ["processing", "ready", "failed"]:
        return "invalid status"

    db.add(video)
    db.commit()
    db.refresh(video)
    return video