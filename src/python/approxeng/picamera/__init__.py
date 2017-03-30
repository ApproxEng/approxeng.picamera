import numpy as np
import cv2


def find_lines(image, threshold=100, scan_region_height=50, scan_region_position=0, scan_region_width_pad=0,
               min_detection_area=100, invert=False):
    """
    Scan a numpy image to find things that look like dark lines on a pale background. Return a sorted sequence of
    locations of line centroids, where (when not inverted) -1.0 corresponds to the left edge of the image, 0 to the 
    centre and 1.0 to the right edge. Centroids are sorted in ascending order.
    
    :param image: 
        A numpy image to process. Grab this with the read method of VideoStream from imutils or similar
    :param threshold: 
        The threshold used to convert to black and white after a gaussian blur is applied, defaults to 100
    :param scan_region_height: 
        The height in pixels of the region to use, defaults to 50
    :param scan_region_position: 
        The position of the region relative to the entire frame. 0 is at the top, 1.0 is as far towards the bottom as it
        will go. Defaults to 0, scanning the top 'scan_region_height' pixels of the image
    :param scan_region_width_pad:
        The number of pixels to discard at either edge of the region, defaults t0 0
    :param min_detection_area:
        The minimum area of detected moments, any feature below this size will be ignored. Defaults to 100 pixels
    :param invert: 
        Boolean - set this to true if your pi camera is upside-down and you therefore want to have -1.0 at the right 
        hand edge of the image rather than the left
    :return: 
        A sequence of float values ranging from -1.0 to 1.0, in ascending order, corresponding to the x coordinate of
        the centroids of any line regions detected
    """
    height = np.size(image, 0)
    width = np.size(image, 1)
    min_row = (height - scan_region_height) * scan_region_position

    # Select a sub-region and convert it to grayscale, we're not interested in colour here
    region = cv2.cvtColor(
        image[min_row:(min_row + scan_region_height), scan_region_width_pad:(width - scan_region_width_pad)],
        cv2.COLOR_BGR2GRAY)
    # Apply a gaussian blur to deal with any noise, this cleans up grain from the camera and removes any tiny
    # features we don't care about
    region = cv2.GaussianBlur(region, (21, 21), 0)
    # Threshold the image, converting it into black and white. Because we previously blurred it this should result
    # in a reasonably clean set of features
    th, region = cv2.threshold(region, threshold, 255, cv2.THRESH_BINARY_INV)
    # Find contours - these are boundaries of regions in the image.
    contoured, contours, heirarchy = cv2.findContours(region, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # We'll populate this with line locations
    lines = []
    # Iterate over the contours. Each contour is a single feature, hopefully a bit of a line; the contour contains the
    # boundary formed from the edge of the region we're sampling as well as the actual line edges.
    for contour in contours:
        # Compute moments of the region.
        m = cv2.moments(contour)
        # Reject any regions which have a smaller area than the minimum. This cleans up larger false hits than the
        # blur operation we did earlier. The 'min_detection_area' needs to be tuned to your particular application, in
        # the case of line followers you'll worry about the height of the sampling region, resolution of the camera and
        # width of the line itself.
        if m['m00'] > min_detection_area:
            # Get the x coordinate of the centroid of the region
            cx = m['m10'] / m['m00']
            # ...and its value on a scale of -1.0 to 1.0
            proportional_cx = 2 * cx / width - 1.0
            # ...and flip it if we said that's what we wanted (i.e. the camera is mounted upside-down)
            if invert:
                proportional_cx = -proportional_cx
            lines.append(proportional_cx)
    # Return a sorted set of x coordinates of detected lines
    return sorted(lines)