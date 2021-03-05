# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")

# Add path to chromedriver executable here
chromedriver_path = "chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)


def login_keats():
    is_logged_in = False
    keats = 'http://keats.kcl.ac.uk/'
    driver.get(keats)
    sleep(1)

    if driver.current_url != "https://keats.kcl.ac.uk/my/":
        try:
            user = input("Whats your k user email?")
            password = input("whats your k password")

            # email box
            user_name = driver.find_element_by_id('i0116')
            if user_name:
                user_name.send_keys(user)

            next1 = driver.find_element_by_id('idSIButton9')
            if next1:
                next1.click()

            # give em rest
            sleep(5)

            # now enter passwd
            user_pass = driver.find_element_by_id('i0118')
            if user_pass:
                user_pass.send_keys(password)

            sign_in = driver.find_element_by_id('idSIButton9')
            if sign_in:
                sign_in.click()

            # check for verification
            input("Press Enter after you have verified the login... ")

            sleep(3)

            next2 = driver.find_element_by_id('idSIButton9')
            if next2:
                next2.click()

            # rest again
            sleep(5)
            is_logged_in = True

        except Exception as ex:
            print(str(ex))
            is_logged_in = False
        finally:
            return is_logged_in
    else:
        driver.get(keats)
        sleep(5)


def get_classes():
    classes = driver.find_elements_by_class_name('coursename')

    starred = []
    for i in classes:
        if "starred" in i.text:
            starred.append(i)

    for i in starred:
        print(i.text[30:])

    classchosen = int(input("Which class? "))

    starred[classchosen - 1].find_element_by_xpath('..').click()


def get_weeks():
    checkforweeks = driver.find_elements_by_class_name('sectionname')
    weeks = []
    for i in checkforweeks:
        if "Week" in i.text:
            weeks.append(i)
            print(i.text)

    week = weeks[int(input("Which week? ")) - 1]

    for i in range(3):
        week = week.find_element_by_xpath('..')

    checklinks = week.find_elements_by_xpath('.//a[contains(@href,"kalvid")]')

    links = []
    for i in checklinks:
        if i:
            links.append(i.get_attribute("href"))
            print(i.text, i.get_attribute("href"))

    videocount = 1

    click = 1 if (input("Would you like to click video? y/n") == "y") else 0

    for i in links:
        subtitles = 0

        driver.get(i)
        # DOWNLOAD THE VIDEOS HERE

         # Changed to id selector as incosistencies with two types of video uploads kalvidres and kalvidpres
        iframe1 = driver.find_element_by_id("contentframe")
        driver.switch_to.frame(iframe1)

        if click:
            driver.find_element_by_tag_name("button").click()
            sleep(4)


        iframe2 = driver.find_element_by_class_name("mwEmbedKalturaIframe")
        driver.switch_to.frame(iframe2)
        video = driver.find_element_by_tag_name("video")

        # Capture video title and rename for order
        videotitle = driver.find_element_by_class_name("truncateText").text
        videotitle = " Video " + str(videocount) + ". " + videotitle

        # Replaces bad symbols with good ones
        bad = ["\\", "/", ":"]
        for x in bad:
            videotitle = videotitle.replace(x, "-")

        sleep(1)

        try:
            subtitles = driver.find_element_by_tag_name("track")
            subtitles = subtitles.get_attribute("src")
        except:
            pass

        video_download_link = video.get_attribute("src")
        driver.get(video_download_link)

        sleep(2)

        if subtitles != 0:
            driver.get(subtitles)
            with open(('C:/Users/moish/Downloads/' + videotitle + '.srt'), 'w', encoding='utf8') as f:
                f.write(driver.find_element_by_tag_name("pre").text)
            sleep(1)

        sleep(0.5)

        os.rename('C:/Users/moish/Downloads/a.m3u8', 'C:/Users/moish/Downloads/' + videotitle + ".m3u8")

        videocount += 1

    # Closes the session
    driver.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    login_keats()

    sleep(1)

    get_classes()

    sleep(1)

    get_weeks()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
